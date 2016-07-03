import enum


class Status(enum.Enum):
    BATTERY_STATUS = 1
    BATTERY_LEVEL = 2

    CURRENT_MODE = 43
    CURRENT_SUB_MODE = 44
    CURRENT_RECORDING_VIDEO_DURATION = 13

    COUNT_CLIENTS_CONNECTED = 31
    STREAMING_FEED_STATUS = 32
    SD_CARD_STATUS = 33
    COUNT_REMAINING_PHOTOS = 34
    COUNT_REMAINING_VIDEO_TIME = 35

    COUNT_BATCH_PHOTOS_TAKEN = 36
    COUNT_VIDEOS_SHOT = 37
    COUNT_PHOTOS_TAKEN = 38

    #wat?
    COUNT_VIDEO_TAKEN = 39
    COUNT_MULTISHOT_PICTURES_TAKEN = 39

    BUSY_STATUS = 8


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