import requests
import re
import json
import pprint
import os
import os.path
import urllib.request

import cameras.HERO4.enum.settings as gpSettings
import cameras.HERO4.enum.status as gpStats


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
        except Exception as e:
            self.connection = 'Not Connected'
            return {}

    def _autoconfigure(self):
        self.gpControl = self._command_api()
        return
        print('Commands:')
        # for cmd in self.gpControl['commands']:
        #    print('Key: {key}\n    Widget: {widget_type} \n    Display: {display_name} \n    URL: {url} \n'.format(widget_type=cmd['widget_type'], display_name=cmd['display_name'], url=cmd['url'], key=cmd['key']))

        for dh in self.gpControl['display_hints']:
            print('\nCategory: {}'.format(dh['display_name']))
            print('    Commands:')
            for cmd in dh['commands']:
                print('        Precedence: {pre}\n        Key: {key}\n        Display: {display}\n'.format(
                    pre=cmd['precedence'], key=cmd['command_key'],
                    display=(self._find_command(cmd['command_key'])['display_name'])))
            print('    Settings:')
            for setting in dh['settings']:
                display_setting = self._find_setting(setting['setting_id'])
                print('        Display Name: {display}\n        Widget Type: {widget}'.format(
                    display=display_setting['display_name'], widget=setting['widget_type']))
                print('        Options:')
                for option in display_setting['options']:
                    print('             Display Name: {display}\n             Value: {value}\n'.format(
                        display=option['display_name'], value=option['value']))

    def _find_command(self, key):
        for cmd in self.gpControl['commands']:
            if str(cmd['key']) == str(key):
                return cmd
        raise NotImplementedError('Command with the key {key} is not available in this GoPro'.format(id=key))

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
            dumptext += '\n\tPath Segment: {ps}\n\t\tDisplay Name: {display_name}\n\t\tValue: {value}\n'.format(ps=mode['path_segment'], display_name=mode['display_name'], value=mode['value'])
            for setting in mode['settings']:
                dumptext += '\n\t\tPath Segment: {ps}\n\t\t\tDisplay Name: {display_name}\n\t\t\tid: {id}\n'.format(ps=setting['path_segment'], display_name=setting['display_name'], id=setting['id'])
                for option in setting['options']:
                    dumptext += '\n\t\t\tOptions:\n\t\t\t\tDisplay Name: {display_name}\n\t\t\t\tValue: {value}\n'.format(display_name=option['display_name'], value=option['value'])
        with open(path, 'w') as f:
            f.write(dumptext)

    def _find_status(self, status_key):
        for group in self.gpControl['status']['groups']:
            for field in group['fields']:
                if str(field['id']) == status_key:
                    return group, field
        raise NotImplementedError(
            'No information to the status value {status} found in this GoPro'.format(status=status_key))

    def print_status(self):
        status = self._command_api('/status')

        _errors = []
        for key in status['status']:
            group, field = self._find_status(key)
            # print('Group: {group} Name: {name} = {value}'.format(name=field['name'].ljust(30),value=status['status'][key],group=group['group'].ljust(20)))
        for setting in status['settings']:
            try:
                stat_setting, option = self._find_value_and_setting(setting, status['settings'][setting])

                # print('Group: {group} Name: {name} = {value}'.format(name=stat_setting['display_name'].ljust(30),value=option['display_name'],group=stat_setting['path_segment'].ljust(20)))
            except:
                _errors.append((setting, status['settings'][setting]))
        for key, value in sorted(_errors, key=lambda setting: setting[0]):
            print("Undocumented Key,Value pair: {key} = {value}".format(key=key, value=value))
            print(status)

    def download_all(self, url='/', path='.'):
        medialist = self._media_api(url)
        folders = re.findall('<a class="link" href="(?P<f>.*?/)">.*?</a>', medialist)
        for folder in folders:
            self.download_all(url + folder, path=path)
        files = re.findall('<a class="link" href="(?P<f>[^/]*?)">.*?</a>', medialist)
        for file in files:
            self.download(url, path + url, file)

    def download(self, url, directory, file, delete_after_download=False):
        gpFilePath = url + file
        url = self._media_url + url + file
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass
        while os.path.isfile(directory + file):
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
                if not delete_after_download:
                    self.delete(gpFilePath)
        except Exception as e:
            print(str(e) + ' at ' + url)

    def delete(self, file):
        self._command_api(method=self._find_command('GPCAMERA_DELETE_FILE_ID')['url'] + '?p=' + file)


if __name__ == '__main__':
    h4 = HERO4()
    h4._autoconfigure()
    h4._find_status()
    h4.dump_all()
    # h4.download_all(path='/media/xyoz/XYOZ-INT1000E/Pictures/2016_07_ScriptedTimelapseExperiments')
