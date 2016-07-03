import enum


class Glue:
    @staticmethod
    def lookup(key, value):
        # Video

        if key == Settings.VIDEO_SUB_MODE or Settings.VIDEO_SUB_MODE.value:
            return VideoSubMode(value)

        if key == Settings.VIDEO_RESOLUTION or Settings.VIDEO_RESOLUTION.value:
            return VideoResolution(value)

        if key == Settings.VIDEO_FRAME_RATE or Settings.VIDEO_FRAME_RATE.value:
            return VideoFrameRate(value)
        
        if key == Settings.VIDEO_FOV or Settings.VIDEO_FOV.value:
            return VideoFOV(value)
        
        if key == Settings.TIMELAPSE_VIDEO_INTERVAL or Settings.TIMELAPSE_VIDEO_INTERVAL.value:
            return TimelapseVideoInterval(value)
        
        if key == Settings.LOOPING_VIDEO_INTERVAL or Settings.LOOPING_VIDEO_INTERVAL.value:
            return LoopingVideoInterval(value)
        
        if key == Settings.VIDEO_LOW_LIGHT or Settings.VIDEO_LOW_LIGHT.value:
            return VideoLowLight(value)
        
        if key == Settings.VIDEO_SPOT_METER or Settings.VIDEO_SPOT_METER.value:
            return VideoSpotMeter(value)
        
        if key == Settings.VIDEO_PROTUNE or Settings.VIDEO_PROTUNE.value:
            return VideoProtune(value)
        
        if key == Settings.WHITE_BALANCE or Settings.WHITE_BALANCE.value:
            return VideoWhiteBalance(value)
        
        if key == Settings.VIDEO_COLOR or Settings.VIDEO_COLOR.value:
            return VideoColor(value)
        
        if key == Settings.VIDEO_ISO_LIMIT or Settings.VIDEO_ISO_LIMIT.value:
            return VideoIsoLimit(value)
        
        if key == Settings.VIDEO_SHARPNESS or Settings.VIDEO_SHARPNESS.value:
            return VideoSharpness(value)
        
        if key == Settings.VIDEO_EV_COMP or Settings.VIDEO_EV_COMP.value:
            return VideoEVComp(value)

        # Photo

        if key == Settings.PHOTO_SUB_MODE or Settings.PHOTO_SUB_MODE.value:
            return PhotoSubMode(value)
        
        if key == Settings.PHOTO_MEGAPIXEL or Settings.PHOTO_MEGAPIXEL.value:
            return PhotoMegapixel(value)
        
        if key == Settings.PHOTO_CONTINUOUS_RATE or Settings.PHOTO_CONTINUOUS_RATE.value:
            return PhotoContinuousRate(value)
        
        if key == Settings.PHOTO_SHUTTER or Settings.PHOTO_SHUTTER.value:
            return PhotoShutter(value)
        
        if key == Settings.PHOTO_SPOT_METER or Settings.PHOTO_SPOT_METER.value:
            return PhotoSpotMeter(value)
        
        if key == Settings.PHOTO_PROTUNE or Settings.PHOTO_PROTUNE.value:
            return PhotoProtune(value)
        
        if key == Settings.WHITE_BALANCE or Settings.WHITE_BALANCE.value:
            return PhotoWhiteBalance(value)
        
        if key == Settings.PHOTO_COLOR or Settings.PHOTO_COLOR.value:
            return PhotoColor(value)
        
        if key == Settings.PHOTO_ISO_LIMIT or Settings.PHOTO_ISO_LIMIT.value:
            return PhotoIsoLimit(value)
        
        if key == Settings.PHOTO_SHARPNESS or Settings.PHOTO_SHARPNESS.value:
            return PhotoSharpness(value)
        
        if key == Settings.PHOTO_EV_COMP or Settings.PHOTO_EV_COMP.value:
            return PhotoEVComp(value)

        if key == Settings.MULTISHOT_SUB_MODE or Settings.MULTISHOT_SUB_MODE.value:
            return MultishotSubMode(value)
        
        if key == Settings.MULTISHOT_DEFAULT_SUB_MODE or Settings.MULTISHOT_DEFAULT_SUB_MODE.value:
            return MultishotDefaultSubMode(value)
        
        if key == Settings.MULTISHOT_NIGHT_SHUTTER_EXPOSURE or Settings.MULTISHOT_NIGHT_SHUTTER_EXPOSURE.value:
            return MultishotNightShutterExposure(value)
        
        if key == Settings.MULTISHOT_BURST_RATE or Settings.MULTISHOT_BURST_RATE.value:
            return MultishotBurstRate(value)
        
        if key == Settings.MULTISHOT_TIMELAPSE_INTERVAL or Settings.MULTISHOT_TIMELAPSE_INTERVAL.value:
            return MultishotTimelapseInterval(value)
        
        if key == Settings.MULTISHOT_NIGHTLAPSE_INTERVAL or Settings.MULTISHOT_NIGHTLAPSE_INTERVAL.value:
            return MultishotNightlapseInterval(value)
        
        if key == Settings.MULTISHOT_MEGAPIXEL or Settings.MULTISHOT_MEGAPIXEL.value:
            return MultishotMegapixel(value)
        
        if key == Settings.MULTISHOT_SPOT_METER or Settings.MULTISHOT_SPOT_METER.value:
            return MultishotSpotMeter(value)
        
        if key == Settings.MULTISHOT_PROTUNE or Settings.MULTISHOT_PROTUNE.value:
            return MultishotProtune(value)
        
        if key == Settings.WHITE_BALANCE or Settings.WHITE_BALANCE.value:
            return MultishotWhiteBalance(value)
        
        if key == Settings.MULTISHOT_COLOR or Settings.MULTISHOT_COLOR.value:
            return MultishotColor(value)
        
        if key == Settings.MULTISHOT_ISO_LIMIT or Settings.MULTISHOT_ISO_LIMIT.value:
            return MultishotIsoLimit(value)
        
        if key == Settings.MULTISHOT_SHARPNESS or Settings.MULTISHOT_SHARPNESS.value:
            return MultishotSharpness(value)
        
        if key == Settings.MULTISHOT_EV_COMP or Settings.MULTISHOT_EV_COMP.value:
            return MultishotEVComp(value)

        # Other

        if key == Settings.LCD_DISPLAY or Settings.LCD_DISPLAY.value:
            return LCDisplay(value)

        if key == Settings.ORIENTATION or Settings.ORIENTATION.value:
            return Orientation(value)

        if key == Settings.DEFAULT_BOOT_MODE or Settings.DEFAULT_BOOT_MODE.value:
            return DefaultBootMode(value)

        if key == Settings.QUICK_CAPTURE or Settings.QUICK_CAPTURE.value:
            return QuickCapture(value)

        if key == Settings.LED_STATUS or Settings.LED_STATUS.value:
            return LEDStatus(value)

        if key == Settings.BEEP_VOLUME or Settings.BEEP_VOLUME.value:
            return BeepVolume(value)

        if key == Settings.VIDEO_FORMAT or Settings.VIDEO_FORMAT.value:
            return VideoFormat(value)

        if key == Settings.ON_SCREEN_DATA or Settings.ON_SCREEN_DATA.value:
            return OnScreenData(value)

        if key == Settings.AUTO_POWER_OFF or Settings.AUTO_POWER_OFF.value:
            return AutoPowerOff(value)


@enum.unique
class Settings(enum.Enum):
    VIDEO_SUB_MODE = 68
    VIDEO_RESOLUTION = 2
    VIDEO_FRAME_RATE = 3
    VIDEO_FOV = 4

    TIMELAPSE_VIDEO_INTERVAL = 5
    LOOPING_VIDEO_INTERVAL = 6
    PHOTO_VIDEO_INTERVAL = 7

    VIDEO_LOW_LIGHT = 8
    VIDEO_SPOT_METER = 9
    VIDEO_PROTUNE = 10
    VIDEO_WHITE_BALANCE = 11
    VIDEO_COLOR = 12
    VIDEO_ISO_LIMIT = 13
    VIDEO_SHARPNESS = 14
    VIDEO_EV_COMP = 15

    PHOTO_SUB_MODE = 69
    PHOTO_MEGAPIXEL = 17
    PHOTO_CONTINUOUS_RATE = 18
    PHOTO_SHUTTER = 19
    PHOTO_SPOT_METER = 20
    PHOTO_PROTUNE = 21
    PHOTO_WHITE_BALANCE = 22
    PHOTO_COLOR = 23
    PHOTO_ISO_LIMIT = 24
    PHOTO_SHARPNESS = 25
    PHOTO_EV_COMP = 26

    MULTISHOT_SUB_MODE = 70
    MULTISHOT_DEFAULT_SUB_MODE = 27
    MULTISHOT_NIGHT_SHUTTER_EXPOSURE = 31
    MULTISHOT_BURST_RATE = 29
    MULTISHOT_TIMELAPSE_INTERVAL = 30
    MULTISHOT_NIGHTLAPSE_INTERVAL = 32
    MULTISHOT_MEGAPIXEL = 28
    MULTISHOT_SPOT_METER = 33
    MULTISHOT_PROTUNE = 34
    MULTISHOT_WHITE_BALANCE = 35
    MULTISHOT_COLOR = 36
    MULTISHOT_SHARPNESS = 38
    MULTISHOT_EV_COMP = 39
    MULTISHOT_ISO_LIMIT = 37

    LCD_DISPLAY = 72
    ORIENTATION = 52
    DEFAULT_BOOT_MODE = 53
    QUICK_CAPTURE = 54
    LED_STATUS = 55
    BEEP_VOLUME = 56
    VIDEO_FORMAT = 57
    ON_SCREEN_DATA = 58
    AUTO_POWER_OFF = 59


class VideoSubMode(enum.Enum):
    VIDEO = 0
    TIMELAPSE_VIDEO = 1
    PHOTO_VIDEO = 2
    LOOPING_VIDEO = 3


class VideoResolution(enum.Enum):
    UHD_4K_SUPER_VIEW = 2
    UHD_4K = 1
    HD_2_7K_SUPER_VIEW = 5
    HD_2_7K = 4
    HD_2_7K_4_3 = 6
    HD_1440 = 7
    HD_1080_SuperView = 8
    HD_1080 = 9
    HD_960 = 10
    HD_720_SuperView = 11
    HD_720 = 11
    WVGA = 13


class VideoFrameRate(enum.Enum):
    FPS_240 = 0
    FPS_120 = 1
    FPS_100 = 2
    FPS_90 = 3
    FPS_80 = 4
    FPS_60 = 5
    FPS_50 = 6
    FPS_48 = 7
    FPS_30 = 8
    FPS_25 = 9
    FPS_24 = 10
    FPS_15 = 11
    FPS_12_5 = 12


class VideoFOV(enum.Enum):
    WIDE = 0
    MEDIUM = 1
    NARROW = 2


class TimelapseVideoInterval(enum.Enum):
    SEC_0_5 = 0
    SEC_1 = 1
    SEC_2 = 2
    SEC_5 = 3
    SEC_10 = 4
    SEC_30 = 5
    SEC_60 = 6


class LoopingVideoInterval(enum.Enum):
    MAXIMUM = 0
    MIN_5 = 1
    MIN_20 = 2
    MIN_60 = 3
    MIN_120 = 4


class PhotoVideoInterval(enum.Enum):
    #maybe rename them, idk what this is
    SEC_5 = 1
    SEC_10 = 2
    SEC_30 = 3
    SEC_60 = 4


class VideoLowLight(enum.Enum):
    ON = 1
    OFF = 0
    
    
class VideoSpotMeter(enum.Enum):
    ON = 1
    OFF = 0
    
    
class VideoProtune(enum.Enum):
    ON = 1
    OFF = 0


class VideoWhiteBalance(enum.Enum):
    AUTO = 0
    WB_3000K = 1
    WB_5500K = 2
    WB_6500K = 3
    NATIVE = 4
    

class VideoColor(enum.Enum):
    GOPRO_COLOR = 0
    FLAT = 1
    

class VideoIsoLimit(enum.Enum):
    ISO_6400 = 0
    ISO_1600 = 1
    ISO_400 = 2
    ISO_3200 = 3
    ISO_800 = 4
    
    
class VideoSharpness(enum.Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2
    
    
class VideoEVComp(enum.Enum):
    MINUS_2 = 8
    MINUS_1_5 = 7
    MINUS_1 = 6
    MINUS_0_5 = 5
    ZERO = 4
    PLUS_0_5 = 3
    PLUS_1 = 2
    PLUS_1_5 = 1
    PLUS_2 = 0


# Photo Settings
class PhotoSubMode(enum.Enum):
    SINGLE = 0
    CONTINUOUS = 1
    NIGHT = 3


class PhotoContinuousRate(enum.Enum):
    FRAMES_3 = 0
    FRAMES_5 = 1
    FRAMES_10 = 2


class PhotoMegapixel(enum.Enum):
    WIDE_12MP = 0
    WIDE_7MP = 1
    MEDIUM_7MP = 2
    MEDIUM_5MP = 3


class PhotoShutter(enum.Enum):
    AUTO = 0
    SEC_2 = 1
    SEC_5 = 2
    SEC_10 = 3
    SEC_15 = 4
    SEC_20 = 5
    SEC_30 = 6


class PhotoSpotMeter(enum.Enum):
    ON = 1
    OFF = 0
    
    
class PhotoProtune(enum.Enum):
    ON = 1
    OFF = 0


class PhotoWhiteBalance(enum.Enum):
    AUTO = 0
    WB_3000K = 1
    WB_5500K = 2
    WB_6500K = 3
    NATIVE = 4
    

class PhotoColor(enum.Enum):
    GOPRO_COLOR = 0
    FLAT = 1
    

class PhotoIsoLimit(enum.Enum):
    ISO_800 = 0
    ISO_400 = 1
    ISO_200 = 2
    ISO_100 = 3
    
    
class PhotoSharpness(enum.Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2
    
    
class PhotoEVComp(enum.Enum):
    MINUS_2 = 8
    MINUS_1_5 = 7
    MINUS_1 = 6
    MINUS_0_5 = 5
    ZERO = 4
    PLUS_0_5 = 3
    PLUS_1 = 2
    PLUS_1_5 = 1
    PLUS_2 = 0


class MultishotSubMode(enum.Enum):
    BURST = 0
    TIMELAPSE = 1
    NIGHTLAPSE = 2


class MultishotDefaultSubMode(enum.Enum):
    BURST = 0
    TIMELAPSE = 1
    NIGHTLAPSE = 2


class MultishotNightShutterExposure(enum.Enum):
    AUTO = 0
    SEC_2 = 1
    SEC_5 = 2
    SEC_10 = 3
    SEC_15 = 4
    SEC_20 = 5
    SEC_30 = 6


class MultishotBurstRate(enum.Enum):
    SEC_1_PHOTO_3 = 0
    SEC_1_PHOTO_5 = 1
    SEC_1_PHOTO_10 = 2
    SEC_2_PHOTO_10 = 3
    SEC_3_PHOTO_10 = 4
    SEC_1_PHOTO_30 = 5
    SEC_2_PHOTO_30 = 6
    SEC_3_PHOTO_30 = 7
    SEC_6_PHOTO_30 = 8


class MultishotTimelapseInterval(enum.Enum):
    SEC_0_5 = 0
    SEC_1 = 1
    SEC_2 = 2
    SEC_5 = 5
    SEC_10 = 10
    SEC_30 = 30
    SEC_60 = 60


class MultishotNightlapseInterval(enum.Enum):
    CONTINUOUS = 0
    SEC_4 = 4
    SEC_5 = 5
    SEC_10 = 10
    SEC_15 = 15
    SEC_20 = 20
    SEC_30 = 30

    SEC_60 = 60
    MIN_1 = 60

    SEC_120 = 120
    MIN_2 = 120

    SEC_300 = 300
    MIN_5 = 300

    SEC_1800 = 1800
    MIN_30 = 1800

    SEC_3600 = 3600
    MIN_60 = 3600


class MultishotMegapixel(enum.Enum):
    WIDE_12MP = 0
    WIDE_7MP = 1
    MEDIUM_7MP = 2
    MEDIUM_5MP = 3


class MultishotSpotMeter(enum.Enum):
    ON = 1
    OFF = 0
    
    
class MultishotProtune(enum.Enum):
    ON = 1
    OFF = 0


class MultishotWhiteBalance(enum.Enum):
    AUTO = 0
    WB_3000K = 1
    WB_5500K = 2
    WB_6500K = 3
    NATIVE = 4
    

class MultishotColor(enum.Enum):
    GOPRO_COLOR = 0
    FLAT = 1
    

class MultishotIsoLimit(enum.Enum):
    ISO_800 = 0
    ISO_400 = 1
    ISO_200 = 2
    ISO_100 = 3
    
    
class MultishotSharpness(enum.Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2
    
    
class MultishotEVComp(enum.Enum):
    MINUS_2 = 8
    MINUS_1_5 = 7
    MINUS_1 = 6
    MINUS_0_5 = 5
    ZERO = 4
    PLUS_0_5 = 3
    PLUS_1 = 2
    PLUS_1_5 = 1
    PLUS_2 = 0

class LCDisplay(enum.Enum):
    ON = 1
    OFF = 0

class Orientation(enum.Enum):
    AUTO = 0
    UP = 1
    DOWN = 2


class DefaultBootMode(enum.Enum):
    VIDEO = 0
    PHOTO = 1
    MULTISHOT = 2


class QuickCapture(enum.Enum):
    ON = 1
    OFF = 0


class LEDStatus(enum.Enum):
    LED_0 = 0
    OFF = 0
    LED_2 = 1
    LED_4 = 2


class BeepVolume(enum.Enum):
    MUTE = 2
    MEDIUM = 1
    PERCENT_70 = 1
    FULL = 0
    PERCENT_100 = 0


class VideoFormat(enum.Enum):
    NTSC = 0
    PAL = 1


class OnScreenData(enum.Enum):
    ON = 1
    OFF = 0


class AutoPowerOff(enum.Enum):
    NEVER = 0
    MIN_1 = 1
    MIN_2 = 2
    MIN_3 = 3
    MIN_5 = 5