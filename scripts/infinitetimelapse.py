import datetime
import time

import goprolib.HERO4.status as gp_stats

import goprolib.HERO4.HERO4 as HERO4
import goprolib.HERO4.settings as gp_settings


def get_suntimes():
    """
    {"coord":{"lon":13.08,"lat":54.31},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}]
    ,"base":"stations","main":{"temp":294.42,"pressure":1020,"humidity":79,"temp_min":290.15,"temp_max":303.15},
    "visibility":10000,"wind":{"speed":5.1,"deg":90},"clouds":{"all":75},"dt":1467810000,"sys":{"type":1,"id":4141,
    "message":0.0319,"country":"DE","sunrise":1467772998,"sunset":1467834077},"id":2826287,"name":"Stralsund","cod":200}

    """
    pass

if __name__ == '__main__':
    h4 = HERO4.HERO4()
    h4.autoconfigure()
    h4.set_mode(gp_stats.App.mode.MULTISHOT, gp_stats.App.sub_mode.NIGHTLAPSE)
    h4.set_setting(gp_settings.Setup.lcd.OFF)
    h4.set_setting(gp_settings.MultiShot.exposure_time.AUTO)
    h4.set_setting(gp_settings.MultiShot.nightlapse_rate.SEC_15)
    h4.set_setting(gp_settings.MultiShot.protune.ON)
    h4.set_setting(gp_settings.MultiShot.protune_sharpness.HIGH)
    h4.set_setting(gp_settings.MultiShot.protune_ev.ZERO)
    h4.set_setting(gp_settings.MultiShot.protune_iso.ISO_100)
    h4.set_setting(gp_settings.MultiShot.protune_color.GOPRO_COLOR)
    h4.set_setting(gp_settings.MultiShot.protune_white_balance.NATIVE)
    h4.shutter(True)
    while True:
        try:
            h4.download_all(delete_after_download=True, path='/media/xyoz/XYOZ-INT1000E/Pictures/2016_07_13 GoPro Auto')
        except:
            print(datetime.datetime.now())
        time.sleep(60)
