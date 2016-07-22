import os
import os.path
import re
import urllib.request
import http.client
import socket
import struct

import logging, logging.config, logging.handlers

import aenum
import goprolib.HERO4.exceptions as gp_exceptions
import goprolib.HERO4.settings as gp_settings
import goprolib.HERO4.status as gp_stats
import requests

import goprolib.HERO4.commands as gp_commands


class HERO4:
    gpControl = {}

    def __init__(self, ip='10.5.5.9', autoconfigure=True):
        self._wol_port = 9
        self._ip = ip
        self._api_url = 'http://' + ip
        self._media_url = self._api_url + '/videos/DCIM'
        if autoconfigure:
            self._autoconfigure()

    def _command_api(self, method='', params='', is_json=True):
        if params:
            params = {'p': params}
        url = self._api_url + '/gp/gpControl' + method
        return self._api_call(url, params, is_json)

    def _media_api(self, path):
        url = self._media_url + path
        return self._api_call(url, '', is_json=False)

    def _api_call(self, url, params, is_json=True):
        try:
            r = requests.get(url, timeout=5.0, params=params)
            self.connection = 'OK'
            if is_json:
                return r.json()
            else:
                return r.text
        except Exception:
            self.connection = 'Not Connected'
            return {}

    @staticmethod
    def _get_enum_value(value):
        """
        If provided value is an enum element, return value of element
        :param value:
        :return:
        """
        if isinstance(value, (aenum.Enum, aenum.EnumMeta, aenum.EnumConstants, aenum.Constant)):
            return value.value
        return value

    # find stuff in gpControl json

    def _find_command(self, key):
        for cmd in self.gpControl['commands']:
            if str(cmd['key']) == str(key):
                return cmd
        raise NotImplementedError('Command with the key {key} is not available in this GoPro'.format(id=key))

    def _find_status(self, status_key):
        for group in self.gpControl['status']['groups']:
            for field in group['fields']:
                if str(field['id']) == status_key:
                    return group, field
        raise NotImplementedError(
            'No information to the status value {status} found in this GoPro'.format(status=status_key))

    def _find_setting(self, setting_key):
        for mode in self.gpControl['modes']:
            for setting in mode['settings']:
                if str(setting['id']) == str(setting_key):
                    return setting
        raise NotImplementedError('Setting with the id {id} is not available in this GoPro'.format(id=setting_key))

    def _find_value_and_setting(self, setting_key, value_key):
        return self._find_value_in_setting(self._find_setting(setting_key), value_key)

    def _find_value_in_setting(self, setting, value_key):
        for option in setting['options']:
            if str(option['value']) == str(value_key):
                return setting, option
        raise NotImplementedError(
            'Option with the value {value} in the setting with the id {setting} is not available in this GoPro'.format(
                value=value_key, setting=setting['id']))


    # load gpControl json (describes api endpoints, key/values, display hints etc)
    def _autoconfigure(self):
        self.gpControl = self._command_api()

    # write api_dump from current gpControl object

    def dump_all(self, path='api_dump', json_path='api_dump.json'):
        dumptext = ''
        dumptext += '\nCommands:'
        for cmd in self.gpControl['commands']:
            dumptext += '\n\tKey: {key}\n\t\tWidget: {widget_type}\n\t\tDisplay: {display_name}\n\t\tURL: {url}\n'.format(
                widget_type=cmd['widget_type'], display_name=cmd['display_name'], url=cmd['url'], key=cmd['key'])

        dumptext += '\nDisplay Hints:'
        for dh in self.gpControl['display_hints']:
            dumptext += '\n\tCategory: {}'.format(dh['display_name'])
            dumptext += '\n\t\tCommands:'
            for cmd in dh['commands']:
                dumptext += ('\n\t\t\tKey: {key}\n\t\t\tDisplay: {display}\n\t\t\tPrecedence: {pre}\n'.format(
                    pre=cmd['precedence'], key=cmd['command_key'],
                    display=(self._find_command(cmd['command_key'])['display_name'])))
            dumptext += '\n\t\tSettings:'
            for setting in dh['settings']:
                display_setting = self._find_setting(setting['setting_id'])
                dumptext += '\n\t\t\tDisplay Name: {display}\n\t\t\tSetting id: {id}\n\t\t\tWidget Type: {widget}'.format(
                    display=display_setting['display_name'], widget=setting['widget_type'], id=setting['setting_id'])
                dumptext += '\n\t\t\tOptions:'
                for option in display_setting['options']:
                    dumptext += '\n\t\t\t\tDisplay Name: {display}\n\t\t\t\tValue: {value}\n'.format(
                        display=option['display_name'], value=option['value'])

        dumptext += '\nModes:'
        for mode in self.gpControl['modes']:
            dumptext += '\n\tPath Segment: {ps}\n\t\tDisplay Name: {display_name}\n\t\tValue: {value}\n'.format(
                ps=mode['path_segment'], display_name=mode['display_name'], value=mode['value'])
            for setting in mode['settings']:
                dumptext += '\n\t\tPath Segment: {ps}\n\t\t\tDisplay Name: {display_name}\n\t\t\tid: {id}\n'.format(
                    ps=setting['path_segment'], display_name=setting['display_name'], id=setting['id'])
                for option in setting['options']:
                    dumptext += '\n\t\t\tOptions:\n\t\t\t\tDisplay Name: {display_name}\n\t\t\t\tValue: {value}\n'.format(
                        display_name=option['display_name'], value=option['value'])

        dumptext += '\nFilters'
        for filter in self.gpControl['filters']:
            dumptext += '\n\tActivated by:'
            for activated_by in filter['activated_by']:
                id = activated_by['setting_id']
                value = activated_by['setting_value']
                id_name = 'Unknown'
                value_name = 'Unknown'
                try:
                    id_name = str(gp_settings.lookup(id))
                except:
                    pass
                else:
                    try:
                        _, value_name = gp_settings.lookup(id,value)
                    except:
                        pass
                dumptext += '\n\t\tSetting ID: {id}\t\t\t{id_name}:\n\t\t\tSetting Value: {value}\t\t{value_name}'.format(
                         id=id, value=value,id_name=id_name,value_name=value_name)
            dumptext += '\n\tBlacklist:'
            blacklistentry = filter['blacklist']
            id = blacklistentry['setting_id']
            id_name = 'Unknown'
            try:
                id_name = str(gp_settings.lookup(id))
            except:
                pass
            dumptext += '\n\t\tSetting ID: {id}\t\t\t{id_name}:'.format(id=id,id_name=id_name)
            for blacklistvalue in blacklistentry['values']:
                value_name = 'Unknown'
                try:
                    if id != 'Unknown':
                        _, value_name = gp_settings.lookup(id,blacklistvalue)
                except:
                    pass
                dumptext += '\n\t\t\tSetting Value: {value}\t\t{value_name}'.format(value=blacklistvalue,value_name=value_name)
            dumptext += '\n'

        with open(path, 'w') as f:
            f.write(dumptext)
        with open(json_path, 'w') as f:
            f.write(self._command_api(is_json=False))

    # load and interpret current camera status (status + settings object) on /status

    def _get_status_with_names(self):
        status = self._command_api('/status')

        _errors = []
        _status = []
        _setting = []

        for key in status['status']:
            try:
                stat_key, stat_val = gp_stats.lookup(key, status['status'][key])
                _status.append((stat_key, stat_val))
            except gp_exceptions.ValueForExistingKeyNotFoundException as e:
                stat_key = e.found_key
                stat_val = e.search_value
                _status.append((stat_key, stat_val))
            except gp_exceptions.KeyNotFoundException as e:
                stat_key = e.search_key
                stat_val = status['status'][key]
                _status.append((stat_key, stat_val))

        for setting in status['settings']:
            try:
                try:
                    sett_key, sett_val = gp_settings.lookup(setting, status['settings'][setting])
                    _setting.append((sett_key, sett_val))
                except gp_exceptions.ValueForExistingKeyNotFoundException as e:
                    sett_key = e.found_key
                    sett_val = e.search_value
                    _setting.append((sett_key, sett_val))
                except gp_exceptions.KeyNotFoundException as e:
                    sett_key = e.search_key
                    sett_val = status['settings'][setting]
                    _errors.append((sett_key, sett_val))
                    # print('Group: {group} Name: {name} = {value}'.format(name=stat_setting['display_name'].ljust(30),value=option['display_name'],group=stat_setting['path_segment'].ljust(20)))
            except:
                _errors.append((setting, status['settings'][setting]))

        return sorted(_status, key=lambda status: str(status[0])), \
               sorted(_setting, key=lambda setting: str(setting[0])), \
               sorted(_errors, key=lambda error: str(error[0]))

    def watch_status(self):
        old_status_obj = None
        old_setting_obj = None
        old_error_obj = None
        while True:
            status_obj, setting_obj, error_obj = self._get_status_with_names()
            if old_status_obj is None and old_error_obj is None and old_setting_obj is None:
                old_status_obj = status_obj
                old_setting_obj = setting_obj
                old_error_obj = error_obj
                self._print_status(status_obj, setting_obj, error_obj)

            # compare status
            for key, value in status_obj:
                for old_key, old_value in old_status_obj:
                    if key.value == old_key.value and str(key) != 'System.CURRENT_TIME_MSEC' and str(
                            key) != 'Setup.DATE_TIME':
                        if value != old_value:
                            print('STATUS: {name}: OLD: {old_val} NEW: {new_val}'.format(name=str(key).ljust(40),
                                                                                         old_val=str(old_value).ljust(
                                                                                             40),
                                                                                         new_val=str(value).ljust(40)))

            # compare setting
            for key, value in setting_obj:
                for old_key, old_value in old_setting_obj:
                    if key.value == old_key.value and str(key) != 'System.CURRENT_TIME_MSEC' and str(
                            key) != 'Setup.DATE_TIME':
                        if value != old_value:
                            print('SETTING: {name}: OLD: {old_val} NEW: {new_val}'.format(name=str(key).ljust(39),
                                                                                          old_val=str(old_value).ljust(
                                                                                              40),
                                                                                          new_val=str(value).ljust(40)))

            # compare errors
            for key, value in error_obj:
                for old_key, old_value in old_error_obj:
                    if key == old_key:
                        if value != old_value:
                            print('UNDOCUMENTED: {name}: OLD: {old_val} NEW: {new_val}'.format(name=str(key).ljust(40),
                                                                                               old_val=str(
                                                                                                   old_value).ljust(5),
                                                                                               new_val=str(value).ljust(
                                                                                                   5)))
            old_status_obj = status_obj
            old_setting_obj = setting_obj
            old_error_obj = error_obj

    def _print_status(self, status_obj=None, setting_obj=None, error_obj=None):
        if status_obj is None and error_obj is None and setting_obj is None:
            status_obj, setting_obj, error_obj = self._get_status_with_names()

        for stat_key, stat_val in status_obj:
            print('STATUS: {name} = {value}'.format(name=str(stat_key).ljust(40), value=stat_val))

        for sett_key, sett_val in setting_obj:
            print('SETTING: {name} = {value}'.format(name=str(sett_key).ljust(39), value=sett_val))

        for key, value in error_obj:
            print("Undocumented Key,Value pair: {key} = {value}".format(key=key, value=value))

    def download_all(self, url='/', path='.', delete_after_download=False):
        medialist = self._media_api(url)
        folders = re.findall('<a class="link" href="(?P<f>.*?/)">.*?</a>', medialist)
        for folder in folders or []:
            self.download_all(url + folder, path=path, delete_after_download=delete_after_download)
        files = re.findall('<a class="link" href="(?P<f>[^/]*?)">.*?</a>', medialist)
        for file in files or []:
            self.download_to_file(url, path + url, file, delete_after_download)

    def download_to_file(self, url, directory, file, delete_after_download=False):
        gp_filepath = url + file
        url = self._media_url + url + file
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass
        while os.path.isfile(directory + file) and file != 'leinfo.sav':
            try:
                filename, ext = file.rsplit(sep='.', maxsplit=1)
            except ValueError:
                file += '_new'
            else:
                file = filename + '_new.' + ext
        try:
            with urllib.request.urlopen(url) as resp, open(directory + file, 'wb') as f:
                data = resp.read()
                f.write(data)
                if delete_after_download:
                    self.delete(gp_filepath)
        except http.client.IncompleteRead as e:
            print('IncompleteRead at ' + directory + file)
            with open(directory + file, 'wb') as f:
                f.write(e.partial)
                if delete_after_download:
                    self.delete(gp_filepath)
        except Exception as e:
            print(str(e) + ' at ' + url)

    def delete(self, file):
        self._command_api(method=gp_commands.Cmd.GPCAMERA_DELETE_FILE_ID.format(file))

    def delete_last(self):
        self._command_api(method=gp_commands.Cmd.GPCAMERA_DELETE_LAST_FILE_ID)

    def delete_all(self):
        self._command_api(method=gp_commands.Cmd.GPCAMERA_DELETE_ALL_FILES_ID)

    def set_mode(self, mode, sub_mode=None, ignore_busy=False):
        mode = self._get_enum_value(mode)
        sub_mode = self._get_enum_value(sub_mode)
        if ignore_busy or not self._is_busy():
            if sub_mode is None:
                self._command_api(gp_commands.Cmd.GPCAMERA_MODE.format(mode))
            else:
                self._command_api(gp_commands.Cmd.GPCAMERA_SUBMODE.format(mode, sub_mode))

    def get_status(self, key):
        key = self._get_enum_value(key)
        return self._command_api('/status')['status'][str(key)]

    def get_setting(self, key):
        key = self._get_enum_value(key)
        return self._command_api('/status')['setting'][str(key)]

    def set_setting(self, value, key=None, ignore_blacklist=False, ignore_busy=False, params=''):
        if key is None:
            try:
                key = gp_settings.reverse_lookup(value)
            except gp_exceptions.KeyNotFoundException:
                return False
        else:
            key = self._get_enum_value(key)
        value = self._get_enum_value(value)
        if ignore_busy or not self._is_busy():
            if ignore_blacklist or self._can(key, value):
                self._command_api(gp_commands.Cmd.GPCAMERA_SETTING.format(key, value), params)

    def shutter(self, capture):
        if capture:
            self._command_api(gp_commands.Cmd.GPCAMERA_SHUTTER.format(1))
        else:
            self._command_api(gp_commands.Cmd.GPCAMERA_SHUTTER.format(0))

    def locate(self, active):
        if active:
            self._command_api(gp_commands.Cmd.GPCAMERA_LOCATE_ID.format(1))
        else:
            self._command_api(gp_commands.Cmd.GPCAMERA_LOCATE_ID.format(0))

    def tag_moment(self):
        self._command_api(gp_commands.Cmd.GPCAMERA_TAG_MOMENT)

    def sleep(self):
        self._command_api(gp_commands.Cmd.GPCAMERA_SLEEP)

    def wakeup(self, mac_address=None):
        if mac_address is None:
            mac_address = self.gpControl['info']['ap_mac']
        else:
            mac_address = str(mac_address)
            if len(mac_address) == 12:
                pass
            elif len(mac_address) == 17:
                sep = mac_address[2]
                mac_address = mac_address.replace(sep, '')
            else:
                raise ValueError('Incorrect MAC address format')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = bytes('FFFFFFFFFFFF' + mac_address * 16, 'utf-8')
        message = b''
        for i in range(0, len(data), 2):
            message += struct.pack(b'B', int(data[i: i + 2], 16))
        sock.sendto(message, (self._ip, self._wol_port))

    def _can(self, key, value, autoconfigure=True):
        key = int(key)
        value = int(value)
        if autoconfigure:
            self._autoconfigure()
        current_settings = self._command_api('/status')['settings']
        for filter in self.gpControl['filters']:
            if int(filter['blacklist']['setting_id']) == key and value in filter['blacklist']['values']:
                filter_passed = False
                for activated_by in filter['activated_by']:
                    if current_settings[str(activated_by['setting_id'])] != activated_by['setting_value']:
                        filter_passed = True
                        break
                if not filter_passed:
                    return False
        return True

    def _is_busy(self):
        self.get_status(gp_stats.System.SYSTEM_BUSY) == gp_stats.System.system_busy.NOT_BUSY

    def start_stream(self, force=False):
        if force or self.get_status(gp_stats.Stream.SUPPORTED) == gp_stats.Stream.supported.SUPPORTED:
            self._command_api(gp_commands.Cmd.GPCAMERA_STREAM.format('start'))

    def stop_stream(self, force=False):
        if force or self.get_status(gp_stats.Stream.ENABLE) == gp_stats.Stream.enable.ENABLED:
            self._command_api(gp_commands.Cmd.GPCAMERA_STREAM.format('stop'))

    def restart_stream(self, force=False):
        if force or self.get_status(gp_stats.Stream.SUPPORTED) == gp_stats.Stream.supported.SUPPORTED:
            self._command_api(gp_commands.Cmd.GPCAMERA_STREAM.format('restart'))



def main():
    h4 = HERO4(autoconfigure=True)
    h4.dump_all()
    h4.watch_status()
    #h4._can(4,2)

if __name__ == '__main__':
    main()
