import requests
import json
import pprint


class HERO4:
    gpControl = {}

    def __init__(self, ip='10.5.5.9'):
        self._ip = ip
        self._api_url = 'http://' + ip
        pass

    def _command_api(self, method='', params=''):
        if params:
            params = {'p': params}
        url = self._api_url + '/gp/gpControl' + method
        return self._api_call(url, params)

    def _api_call(self, url, params):
        try:
            r = requests.get(url, timeout=5.0, params=params)
            self.connection = 'OK'
            return r.json()
        except:
            self.connection = 'Not Connected'
            return {}

    def _autoconfigure(self):
        self.gpControl = self._command_api()

    def _find_command(self, key):
        for cmd in self.gpControl['commands']:
            if cmd['key'] == key:
                return cmd

    def _find_setting(self, key):
        for mode in self.gpControl['modes']:
            for setting in mode['settings']:
                if setting['id'] == key:
                    return setting

    def _test_output_gui(self):
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

if __name__ == '__main__':
    h4 = HERO4()
    h4._autoconfigure()
    h4._test_output_gui()

