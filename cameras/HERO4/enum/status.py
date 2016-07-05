import enum


class Status():
    # Wireless
    class Wireless(enum.Enum):
        ENABLE = 17
        PAIR_STATE = 19
        PAIR_TYPE = 20
        PAIR_TIME = 21

        SCAN_STATE = 22
        SCAN_TIME_MSEC = 23

        PAIRING = 28
        REMOTE_CONTROL_VERSION = 26
        REMOTE_CONTROL_CONNECTED = 27

        APP_COUNT = 31
        PROVISION_STATUS = 24

        WLAN_SSID = 29
        AP_SSID = 30
        WIFI_BARS = 56

    # Stream
    class Stream(enum.Enum):
        ENABLE = (32, 'enable display text')
        SUPPORTED = (55, 'supported display text')

    # Storage
    class Storage(enum.Enum):
        SD_STATUS = 33
        REMAINING_PHOTOS = 34
        REMAINING_VIDEO_TIME = 35
        REMAINING_SPACE = 54

        NUM_GROUP_PHOTOS = 36
        NUM_GROUP_VIDEO = 37
        NUM_TOTAL_PHOTOS = 38
        NUM_TOTAL_VIDEOS = 39




class BatteryStatus(enum.Enum):
    BATTERY_UNAVAILABLE = 0
    BATTERY_AVAILABLE = 1


class BatteryLevel(enum.Enum):
    LOW = 1
    HALFWAY = 2
    FULL = 3
    CHARGING = 4


class CurrentMode(enum.Enum):
    VIDEO = 0
    PHOTO = 1
    MULTISHOT = 2


class CurrentSubMode(enum.Enum):
    # Enum returns on search by value only the first found
    # => Introducing generic results

    FIRST_SUB_MODE = 0
    SECOND_SUB_MODE = 1
    THIRD_SUB_MODE = 2
    FORTH_SUB_MODE = 4

    VIDEO = 0
    SINGLE_PIC = 0
    BURST = 0

    TIMELAPSE_VIDEO = 1
    CONTINUOUS = 1
    TIMELAPSE = 1

    VIDEO_PHOTO = 2
    NIGHT_PHOTO = 2
    NIGHTLAPSE = 2


class StreamingFeedStatus(enum.Enum):
    STREAMING_ACTIVE = 1
    STREAMING_NOT_ACTIVE = 0


class BusyStatus(enum.Enum):
    BUSY = 1
    NOT_BUSY = 0