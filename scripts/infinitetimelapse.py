import cameras.HERO4.HERO4 as HERO4

import cameras.HERO4.enum.status as gp_stats
import cameras.HERO4.enum.settings as gp_settings

import time

if __name__ == '__main__':
    h4 = HERO4.HERO4()
    h4.autoconfigure()
    h4.set_mode(gp_stats.App.mode.MULTISHOT, gp_stats.App.sub_mode.NIGHTLAPSE)
    h4.set_setting(gp_settings.MultiShot.exposure_time.SEC_5)
    h4.set_setting(gp_settings.MultiShot.nightlapse_rate.SEC_10)
    h4.shutter(True)
    while True:
        h4.download_all(delete_after_download=True, path='/media/xyoz/XYOZ-INT1000E/Pictures/2016_07_06 GoPro RPI')
        time.sleep(30)
