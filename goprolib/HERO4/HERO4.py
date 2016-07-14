import os
import os.path
import re
import urllib.request

import aenum
import goprolib.HERO4.exceptions as gp_exceptions
import goprolib.HERO4.settings as gp_settings
import goprolib.HERO4.status as gp_stats
import requests

import goprolib.HERO4.commands as gp_commands


class HERO4:
    gpControl = {}

    def __init__(self, ip='10.5.5.9'):
        self._ip = ip
        self._api_url = 'http://' + ip
        self._media_url = self._api_url + '/videos/DCIM'
        pass

    def _command_api(self, method='', params=''):
        if params:
            params = {'p': params}
        url = self._api_url + '/gp/gpControl' + method
        return self._api_call(url, params)

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
    def autoconfigure(self):
        self.gpControl = self._command_api()

    # write api_dump from current gpControl object

    def dump_all(self, path='api_dump'):
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
        with open(path, 'w') as f:
            f.write(dumptext)

    # load and interpret current camera status (status + settings object) on /status

    def _get_status(self):
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
            status_obj, setting_obj, error_obj = self._get_status()
            if old_status_obj is None and old_error_obj is None and old_setting_obj is None:
                old_status_obj = status_obj
                old_setting_obj = setting_obj
                old_error_obj = error_obj
                self.print_status(status_obj, setting_obj, error_obj)

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

    def print_status(self, status_obj=None, setting_obj=None, error_obj=None):
        if status_obj is None and error_obj is None and setting_obj is None:
            status_obj, setting_obj, error_obj = self._get_status()

        for stat_key, stat_val in status_obj:
            print('STATUS: {name} = {value}'.format(name=str(stat_key).ljust(40), value=stat_val))

        for sett_key, sett_val in setting_obj:
            print('SETTING: {name} = {value}'.format(name=str(sett_key).ljust(39), value=sett_val))

        for key, value in error_obj:
            print("Undocumented Key,Value pair: {key} = {value}".format(key=key, value=value))

    def download_all(self, url='/', path='.', delete_after_download=False):
        medialist = self._media_api(url)
        folders = re.findall('<a class="link" href="(?P<f>.*?/)">.*?</a>', medialist)
        for folder in folders:
            self.download_all(url + folder, path=path, delete_after_download=delete_after_download)
        files = re.findall('<a class="link" href="(?P<f>[^/]*?)">.*?</a>', medialist)
        for file in files:
            self.download(url, path + url, file, delete_after_download)

    def download(self, url, directory, file, delete_after_download=False):
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
        except Exception as e:
            print(str(e) + ' at ' + url)

    def delete(self, file):
        self._command_api(method=gp_commands.Cmd.GPCAMERA_DELETE_FILE_ID.format(file))

    def set_mode(self, mode, sub_mode=None):
        mode = self._get_enum_value(mode)
        sub_mode = self._get_enum_value(sub_mode)
        if sub_mode is None:
            self._command_api(gp_commands.Cmd.GPCAMERA_MODE.format(mode))
        else:
            self._command_api(gp_commands.Cmd.GPCAMERA_SUBMODE.format(mode, sub_mode))

    def set_setting(self, value, key=None, params=''):
        if key is None:
            try:
                key = gp_settings.reverse_lookup(value)
            except gp_exceptions.KeyNotFoundException:
                return False
        else:
            key = self._get_enum_value(key)
        value = self._get_enum_value(value)
        self._command_api(gp_commands.Cmd.GPCAMERA_SETTING.format(key, value), params)

    def shutter(self, capture):
        if capture:
            self._command_api(gp_commands.Cmd.GPCAMERA_SHUTTER.format(1))
        else:
            self._command_api(gp_commands.Cmd.GPCAMERA_SHUTTER.format(0))


def main():
    h4 = HERO4()
    h4.autoconfigure()
    h4.watch_status()
    # h4.dump_all()

if __name__ == '__main__':
    main()