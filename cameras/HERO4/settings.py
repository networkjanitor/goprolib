import enum


class Glue(enum.Enum):
    @staticmethod
    def lookup(key, value):
        if key == Settings.VIDEO_LOW_LIGHT:
            return VideoLowLight(value)


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
    QICK_CAPTURE = 54
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