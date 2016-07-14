import inspect
import sys

import aenum

import goprolib.HERO4.exceptions as enum_exceptions

"""
How keys and values are structured:

Keys are found in different aenum.Enum derived classes inside of this module.
All keys need to be named in uppercase letters.

For each key there can be a value class (again, aenum.Enum derived). This value class needs to be inside the class
the key was found in. Furthermore the name of the value-class need to be lower case. In the future this should be
changed to CamelCase, but I did not found a reliable snake_case to CamelCase converter in time. Feel free to add one.

To make a search for a key or a key-value pair use the method lookup.


Examples:

Stream.ENABLE # Enable property of Stream
Stream.enable.ENABLED # Stream is enabled
Stream.enable.DISABLED # Stream is disabled

Disadventages of this style:

There is no verification, that each key only occurs once in this module. Example:


class TestGroup1(aenum.Enum):
    @aenum.skip
    class test_attribute(aenum.Enum):
        FIZZ = 1
        BUZZ = 0
    TEST_ATTRIBUTE = 42

class TestGroup2(aenum.Enum):
    @aenum.skip
    class test_attribute(aenum.Enum):
        ENABLED = 1
        DISABLED = 0
    TEST_ATTRIBUTE = 42

lookup(42, 1) will return test_attribute.FIZZ
This is because enums will only return the first value which matches the search.
"""


def lookup(key, value=None):
    """
    Search in all classes inside this module.
    """
    for found_key_class in inspect.getmembers(sys.modules[__name__], predicate=inspect.isclass):
        try:
            # Try to find key in class
            # If key is not found in the class, it raises an exception which starts the search in the next class
            key_lookup = _find(key, found_key_class[1])

            # Key found
            if value is not None:
                # Key and value requested

                # Search for the class which has the key name as class name (lower case)
                # The can only be one class with the name
                found_value_class = inspect.getmembers(key_lookup, predicate=lambda elem:
                _nested_name_predicate(elem, key_lookup.name.lower()))
                try:
                    value_lookup = _find(value, found_value_class[0][1])
                    # If such class exists and the value is found within it, return results for key and value
                    return key_lookup, value_lookup
                except:
                    # If such class exists, but the value is not found within it, catch exception and join case
                    # together with the case that no such class exists
                    pass
                # No such class exists, raise exception with the found result for the key
                raise enum_exceptions.ValueForExistingKeyNotFoundException(key, value, key_lookup)
            else:
                # Only key requested
                return key_lookup
        except enum_exceptions.KeyNotFoundException:
            # The key way not found in this class, catch exception and proceed to next class
            pass
    # Key was not found in any classes inside of this module, raise exception and exit
    raise enum_exceptions.KeyNotFoundException(search_key=key)


def reverse_lookup(key):
    # Initialise result variable
    last_key_found = None
    try:
        # Define first search space for inspect.getmembers()
        search_space = sys.modules[__name__]
        # Prepare qualname parts, transform lower 'value enum'-name to upper 'key-value pair'-name.
        qname_parts = key.__class__.__qualname__.split('.')
        qname_parts[-1] = qname_parts[-1].upper()
        # Step into qualname path
        for qname_part in qname_parts:
            # Search for the member of the class with the name of the qualname part
            for found_key_class in inspect.getmembers(search_space,
                                                      predicate=lambda elem: _nested_qualname_predicate(elem,
                                                                                                        qname_part)):
                # Assign found key to result variable
                last_key_found = found_key_class
                # Set search space to found class
                search_space = found_key_class[1]
    except:
        # Something went wrong. Method was probably called with an enum key (e.g. App.ENABLE) instead
        # of an enum value (e.g. App.enable.ENABLED)
        raise enum_exceptions.KeyNotFoundException(key)
    else:
        if last_key_found is not None:
            return last_key_found[1].value
        else:
            raise enum_exceptions.KeyNotFoundException(key)


def _find(key, searchenum):
    try:
        for item in list(searchenum):
            if str(key) == str(item.value):
                return item
    except Exception:
        pass
    raise enum_exceptions.KeyNotFoundException(search_key=key)


def _nested_name_predicate(elem, name):
    try:
        if elem is not None and elem.__name__ == name:
            return True
    except:
        pass
    return False


def _nested_qualname_predicate(elem, name):
    try:
        if elem is not None and elem.__qualname__.rsplit('.', maxsplit=1)[-1] == name:
            return True
    except:
        try:
            if elem is not None and elem.name == name:
                return True
        except:
            pass
        pass
    return False


# Video
class Video(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class default_sub_mode(aenum.Enum):
        VIDEO = 0
        TIMELAPSE_VIDEO = 1
        VIDEO_AND_PHOTO = 2
        LOOPING = 3

    DEFAULT_SUB_MODE = 1

    # noinspection PyPep8Naming
    @aenum.skip
    class current_sub_mode(aenum.Enum):
        VIDEO = 0
        TIMELAPSE_VIDEO = 1
        VIDEO_AND_PHOTO = 2
        LOOPING = 3

    CURRENT_SUB_MODE = 68

    # noinspection PyPep8Naming
    @aenum.skip
    class resolution(aenum.Enum):
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

    RESOLUTION = 2

    # noinspection PyPep8Naming
    @aenum.skip
    class fps(aenum.Enum):
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

    FPS = 3

    # noinspection PyPep8Naming
    @aenum.skip
    class fov(aenum.Enum):
        WIDE = 0
        MEDIUM = 1
        NARROW = 2

    FOV = 4

    # noinspection PyPep8Naming
    @aenum.skip
    class timelapse_rate(aenum.Enum):
        SEC_0_5 = 0
        SEC_1 = 1
        SEC_2 = 2
        SEC_5 = 3
        SEC_10 = 4
        SEC_30 = 5
        SEC_60 = 6

    TIMELAPSE_RATE = 5

    # noinspection PyPep8Naming
    @aenum.skip
    class looping(aenum.Enum):
        MAXIMUM = 0
        MIN_5 = 1
        MIN_20 = 2
        MIN_60 = 3
        MIN_120 = 4

    LOOPING = 6

    # noinspection PyPep8Naming
    @aenum.skip
    class piv(aenum.Enum):
        SEC_5 = 1
        SEC_10 = 2
        SEC_30 = 3
        SEC_60 = 4

    PIV = 7

    # noinspection PyPep8Naming
    @aenum.skip
    class low_light(aenum.Enum):
        OFF = 0
        ON = 1

    LOW_LIGHT = 8

    # noinspection PyPep8Naming
    @aenum.skip
    class spot_meter(aenum.Enum):
        OFF = 0
        ON = 1

    SPOT_METER = 9

    # noinspection PyPep8Naming
    @aenum.skip
    class protune(aenum.Enum):
        OFF = 0
        ON = 1

    PROTUNE = 10

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_white_balance(aenum.Enum):
        AUTO = 0
        WB_3000K = 1
        WB_5500K = 2
        WB_6500K = 3
        NATIVE = 4

    PROTUNE_WHITE_BALANCE = 11

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_color(aenum.Enum):
        GOPRO_COLOR = 0
        FLAT = 1

    PROTUNE_COLOR = 12

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_sharpness(aenum.Enum):
        HIGH = 0
        MEDIUM = 1
        LOW = 2

    PROTUNE_SHARPNESS = 14

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_ev(aenum.Enum):
        MINUS_2 = 8
        MINUS_1_5 = 7
        MINUS_1 = 6
        MINUS_0_5 = 5
        ZERO = 4
        PLUS_0_5 = 3
        PLUS_1 = 2
        PLUS_1_5 = 1
        PLUS_2 = 0

    PROTUNE_EV = 15

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_iso(aenum.Enum):
        ISO_6400 = 0
        ISO_1600 = 1
        ISO_400 = 2
        ISO_3200 = 3
        ISO_800 = 4

    PROTUNE_ISO = 13


# Photo
class Photo(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class default_sub_mode(aenum.Enum):
        SINGLE = 0
        CONTINUOUS = 1
        NIGHT = 2

    DEFAULT_SUB_MODE = 16

    # noinspection PyPep8Naming
    @aenum.skip
    class current_sub_mode(aenum.Enum):
        SINGLE = 0
        CONTINUOUS = 1
        NIGHT = 2

    CURRENT_SUB_MODE = 69

    # noinspection PyPep8Naming
    @aenum.skip
    class continuous_rate(aenum.Enum):
        FRAMES_3_SECOND_1 = 0
        FRAMES_5_SECOND_1 = 1
        FRAMES_10_SECOND_1 = 2

    CONTINUOUS_RATE = 18

    # noinspection PyPep8Naming
    @aenum.skip
    class resolution(aenum.Enum):
        WIDE_12MP = 0
        WIDE_7MP = 1
        MEDIUM_7MP = 2
        MEDIUM_5MP = 3

    RESOLUTION = 17

    # noinspection PyPep8Naming
    @aenum.skip
    class exposure_time(aenum.Enum):
        AUTO = 0
        SEC_2 = 1
        SEC_5 = 2
        SEC_10 = 3
        SEC_15 = 4
        SEC_20 = 5
        SEC_30 = 6

    EXPOSURE_TIME = 19

    # noinspection PyPep8Naming
    @aenum.skip
    class spot_meter(aenum.Enum):
        OFF = 0
        ON = 1

    SPOT_METER = 20

    # noinspection PyPep8Naming
    @aenum.skip
    class protune(aenum.Enum):
        OFF = 0
        ON = 1

    PROTUNE = 21

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_white_balance(aenum.Enum):
        AUTO = 0
        WB_3000K = 1
        WB_5500K = 2
        WB_6500K = 3
        NATIVE = 4

    PROTUNE_WHITE_BALANCE = 22

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_color(aenum.Enum):
        GOPRO_COLOR = 0
        FLAT = 1

    PROTUNE_COLOR = 23

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_sharpness(aenum.Enum):
        HIGH = 0
        MEDIUM = 1
        LOW = 2

    PROTUNE_SHARPNESS = 25

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_ev(aenum.Enum):
        MINUS_2 = 8
        MINUS_1_5 = 7
        MINUS_1 = 6
        MINUS_0_5 = 5
        ZERO = 4
        PLUS_0_5 = 3
        PLUS_1 = 2
        PLUS_1_5 = 1
        PLUS_2 = 0

    PROTUNE_EV = 26

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_iso(aenum.Enum):
        ISO_800 = 0
        ISO_400 = 1
        ISO_200 = 2
        ISO_100 = 3

    PROTUNE_ISO = 24


# MultiShot
class MultiShot(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class default_sub_mode(aenum.Enum):
        BURST = 0
        TIMELAPSE = 1
        NIGHTLAPSE = 2

    DEFAULT_SUB_MODE = 27

    # noinspection PyPep8Naming
    @aenum.skip
    class current_sub_mode(aenum.Enum):
        BURST = 0
        TIMELAPSE = 1
        NIGHTLAPSE = 2

    CURRENT_SUB_MODE = 69

    # noinspection PyPep8Naming
    @aenum.skip
    class exposure_time(aenum.Enum):
        AUTO = 0
        SEC_2 = 1
        SEC_5 = 2
        SEC_10 = 3
        SEC_15 = 4
        SEC_20 = 5
        SEC_30 = 6

    EXPOSURE_TIME = 31

    # noinspection PyPep8Naming
    @aenum.skip
    class burst_rate(aenum.Enum):
        SEC_1_PHOTO_3 = 0
        SEC_1_PHOTO_5 = 1
        SEC_1_PHOTO_10 = 2
        SEC_2_PHOTO_10 = 3
        SEC_3_PHOTO_10 = 4
        SEC_1_PHOTO_30 = 5
        SEC_2_PHOTO_30 = 6
        SEC_3_PHOTO_30 = 7
        SEC_6_PHOTO_30 = 8

    CONTINUOUS_RATE = 29

    # noinspection PyPep8Naming
    @aenum.skip
    class timelapse_rate(aenum.Enum):
        SEC_0_5 = 0
        SEC_1 = 1
        SEC_2 = 2
        SEC_5 = 5
        SEC_10 = 10
        SEC_30 = 30
        SEC_60 = 60

    TIMELAPSE_RATE = 30

    # noinspection PyPep8Naming
    @aenum.skip
    class nightlapse_rate(aenum.Enum):
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

    NIGHTLAPSE_RATE = 32

    # noinspection PyPep8Naming
    @aenum.skip
    class resolution(aenum.Enum):
        WIDE_12MP = 0
        WIDE_7MP = 1
        MEDIUM_7MP = 2
        MEDIUM_5MP = 3

    RESOLUTION = 28

    # noinspection PyPep8Naming
    @aenum.skip
    class spot_meter(aenum.Enum):
        OFF = 0
        ON = 1

    SPOT_METER = 33

    # noinspection PyPep8Naming
    @aenum.skip
    class protune(aenum.Enum):
        OFF = 0
        ON = 1

    PROTUNE = 34

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_white_balance(aenum.Enum):
        AUTO = 0
        WB_3000K = 1
        WB_5500K = 2
        WB_6500K = 3
        NATIVE = 4

    PROTUNE_WHITE_BALANCE = 35

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_color(aenum.Enum):
        GOPRO_COLOR = 0
        FLAT = 1

    PROTUNE_COLOR = 36

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_sharpness(aenum.Enum):
        HIGH = 0
        MEDIUM = 1
        LOW = 2

    PROTUNE_SHARPNESS = 38

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_ev(aenum.Enum):
        MINUS_2 = 8
        MINUS_1_5 = 7
        MINUS_1 = 6
        MINUS_0_5 = 5
        ZERO = 4
        PLUS_0_5 = 3
        PLUS_1 = 2
        PLUS_1_5 = 1
        PLUS_2 = 0

    PROTUNE_EV = 39

    # noinspection PyPep8Naming
    @aenum.skip
    class protune_iso(aenum.Enum):
        ISO_800 = 0
        ISO_400 = 1
        ISO_200 = 2
        ISO_100 = 3

    PROTUNE_ISO = 37


# Setup
class Setup(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class lcd(aenum.Enum):
        OFF = 0
        ON = 1

    LCD = 72

    # noinspection PyPep8Naming
    @aenum.skip
    class lcd_brightness(aenum.Enum):
        HIGH = 0
        MEDIUM = 1
        LOW = 2

    LCD_BRIGHTNESS = 49

    # noinspection PyPep8Naming
    @aenum.skip
    class lcd_lock(aenum.Enum):
        OFF = 0
        ON = 1

    LCD_LOCK = 50

    # noinspection PyPep8Naming
    @aenum.skip
    class lcd_sleep(aenum.Enum):
        NEVER = 0
        MIN_1 = 1
        MIN_2 = 2
        MIN_3 = 3

    LCD_SLEEP = 51

    # noinspection PyPep8Naming
    @aenum.skip
    class orientation(aenum.Enum):
        AUTO = 0
        UP = 1
        DOWN = 2

    ORIENTATION = 52

    # noinspection PyPep8Naming
    @aenum.skip
    class default_app_mode(aenum.Enum):
        VIDEO = 0
        PHOTO = 1
        MULTI_SHOT = 2

    DEFAULT_APP_MODE = 53

    # noinspection PyPep8Naming
    @aenum.skip
    class quick_capture(aenum.Enum):
        OFF = 0
        ON = 1

    QUICK_CAPTURE = 54

    # noinspection PyPep8Naming
    @aenum.skip
    class led(aenum.Enum):
        OFF = 0
        LED_2 = 1
        LED_4 = 2

    LED = 55

    # noinspection PyPep8Naming
    @aenum.skip
    class beep_volume(aenum.Enum):
        MUTE = 2
        MEDIUM = 1
        PERCENT_70 = 1
        FULL = 0
        PERCENT_100 = 0

    BEEP_VOLUME = 56

    # noinspection PyPep8Naming
    @aenum.skip
    class video_format(aenum.Enum):
        NTSC = 0
        PAL = 1

    VIDEO_FORMAT = 57

    # noinspection PyPep8Naming
    @aenum.skip
    class osd(aenum.Enum):
        OFF = 0
        ON = 1

    OSD = 58

    # noinspection PyPep8Naming
    @aenum.skip
    class auto_power_down(aenum.Enum):
        NEVER = 0
        MIN_1 = 1
        MIN_2 = 2
        MIN_3 = 3
        MIN_5 = 5

    AUTO_POWER_DOWN = 58

    # noinspection PyPep8Naming
    @aenum.skip
    class wireless_mode(aenum.Enum):
        OFF = 0
        APP = 1
        RC = 2
        SMART = 4

    WIRELESS_MODE = 63

    # noinspection PyPep8Naming
    @aenum.skip
    class stream_gop_size(aenum.Enum):
        DEFAULT = 0
        VALUE_3 = 3
        VALUE_4 = 4
        VALUE_8 = 8
        VALUE_15 = 15
        VALUE_30 = 30

    STREAM_GOP_SIZE = 60

    # noinspection PyPep8Naming
    @aenum.skip
    class stream_idr_interval(aenum.Enum):
        DEFAULT = 0
        VALUE_1 = 1
        VALUE_2 = 2
        VALUE_4 = 4

    STREAM_IDR_INTERVAL = 61

    # noinspection PyPep8Naming
    @aenum.skip
    class stream_bit_rate(aenum.Enum):
        KBIT_PS_250 = 250000
        KBIT_PS_400 = 400000
        KBIT_PS_600 = 600000
        KBIT_PS_700 = 700000
        KBIT_PS_800 = 800000
        MBIT_PS_1 = 1000000
        MBIT_PS_1_2 = 1200000
        MBIT_PS_1_6 = 1600000
        MBIT_PS_2 = 2000000
        MBIT_PS_2_4 = 2400000

    STREAM_BIT_RATE = 62

    # noinspection PyPep8Naming
    @aenum.skip
    class stream_window_size(aenum.Enum):
        DR_240 = 1
        DR_240_3_4_SUBSAMPLE = 2
        DR_240_1_2_SUBSAMPLE = 3
        DR_480 = 4
        DR_480_3_4_SUBSAMPLE = 5
        DR_480_1_2_SUBSAMPLE = 6

    STREAM_WINDOW_SIZE = 64


if __name__ == '__main__':
    key = None
    value = None
    try:
        x = Video(Video.current_sub_mode).current_sub_mode()

        key, value = lookup(19, 0)
        print(key)
        print(value)
    except enum_exceptions.ValueForExistingKeyNotFoundException as e:
        print(key)
        print(e)
