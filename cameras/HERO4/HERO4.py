import requests
import re
import json
import pprint
import os
import os.path
import urllib.request


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
        #for cmd in self.gpControl['commands']:
        #    print('Key: {key}\n    Widget: {widget_type} \n    Display: {display_name} \n    URL: {url} \n'.format(widget_type=cmd['widget_type'], display_name=cmd['display_name'], url=cmd['url'], key=cmd['key']))

        for dh in self.gpControl['display_hints']:
            print('\nCategory: {}'.format(dh['display_name']))
            print('    Commands:')
            for cmd in dh['commands']:
                print('        Precedence: {pre}\n        Key: {key}\n        Display: {display}\n'.format(pre=cmd['precedence'],key=cmd['command_key'],display=(self._find_command(cmd['command_key'])['display_name'])))
            print('    Settings:')
            for setting in dh['settings']:
                display_setting = self._find_setting(setting['setting_id'])
                print('        Display Name: {display}\n        Widget Type: {widget}'.format(display=display_setting['display_name'],widget=setting['widget_type']))
                print('        Options:')
                for option in display_setting['options']:
                    print('             Display Name: {display}\n             Value: {value}\n'.format(display=option['display_name'],value=option['value']))

    def _find_command(self, key):
        for cmd in self.gpControl['commands']:
            if cmd['key'] == key:
                return cmd
        raise NotImplementedError('Command with the key {key} is not available in this GoPro'.format(id=key))

    def _find_setting(self, setting_key):
        for mode in self.gpControl['modes']:
            for setting in mode['settings']:
                if str(setting['id']) == setting_key:
                    return setting
        raise NotImplementedError('Setting with the id {id} is not available in this GoPro'.format(id=setting_key))

    def _find_value_and_setting(self, setting_key, value_key):
        return self._find_value_in_setting(self._find_setting(setting_key), value_key)

    def _find_value_in_setting(self, setting, value_key):
        for option in setting['options']:
            if option['value'] == value_key:
                return setting,option
        raise NotImplementedError('Option with the value {value} in the setting with the id {setting} is not available in this GoPro'.format(value=value_key,setting=setting['id']))

    def _find_status(self, status_key):
        for group in self.gpControl['status']['groups']:
            for field in group['fields']:
                if str(field['id']) == status_key:
                    return group,field
        raise NotImplementedError('No information to the status value {status} found in this GoPro'.format(status=status_key))

    def print_status(self):
        status = self._command_api('/status')

        _errors = []
        for key in status['status']:
            group,field = self._find_status(key)
            print('Group: {group} Name: {name} = {value}'.format(name=field['name'].ljust(30),value=status['status'][key],group=group['group'].ljust(20)))
        for setting in status['settings']:
            try:
                stat_setting,option = self._find_value_and_setting(setting,status['settings'][setting])
            except:
                _errors.append((setting,status['settings'][setting]))
        for key,value in sorted(_errors,key=lambda setting: setting[0]):
            print("Undocumented Key,Value pair: {key} = {value}".format(key=key,value=value))
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
                filename, ext = file.rsplit(sep='.',maxsplit=1)
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
            print(str(e) + ' at '  + url)

    def delete(self, file):
        self._command_api(method=self._find_command('GPCAMERA_DELETE_FILE_ID')['url'] + '?p=' + file)

if __name__ == '__main__':
    h4 = HERO4()
    h4._autoconfigure()
    h4.print_status()
    #h4.download_all(path='/media/xyoz/XYOZ-INT1000E/Pictures/2016_07_ScriptedTimelapseExperiments')

