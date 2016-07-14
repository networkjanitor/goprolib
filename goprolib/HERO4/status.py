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


# System
class System(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class internal_battery_present(aenum.Enum):
        NOT_PRESENT = 0
        PRESENT = 1

    INTERNAL_BATTERY_PRESENT = 1

    # noinspection PyPep8Naming
    @aenum.skip
    class internal_battery_level(aenum.Enum):
        LOW = 1
        HALFWAY = 2
        FULL = 3
        CHARGING = 4

    INTERNAL_BATTERY_LEVEL = 2

    # noinspection PyPep8Naming
    @aenum.skip
    class external_battery_present(aenum.Enum):
        NOT_PRESENT = 0
        PRESENT = 1

    EXTERNAL_BATTERY_PRESENT = 3

    # noinspection PyPep8Naming
    @aenum.skip
    class external_battery_level(aenum.Enum):
        LOW = 1
        HALFWAY = 2
        FULL = 3
        CHARGING = 4

    EXTERNAL_BATTERY_LEVEL = 4

    # noinspection PyPep8Naming
    @aenum.skip
    class system_hot(aenum.Enum):
        NOT_HOT = 0
        HOT = 1

    SYSTEM_HOT = 6

    # noinspection PyPep8Naming
    @aenum.skip
    class system_busy(aenum.Enum):
        NOT_BUSY = 0
        BUSY = 1

    SYSTEM_BUSY = 8

    # noinspection PyPep8Naming
    @aenum.skip
    class quick_capture_active(aenum.Enum):
        pass

    QUICK_CAPTURE_ACTIVE = 9

    # noinspection PyPep8Naming
    @aenum.skip
    class encoding_active(aenum.Enum):
        # TODO: EXPERIMENTAL: ENCODING ACTIVE
        ACTIVE = 1
        NOT_ACTIVE = 0

    ENCODING_ACTIVE = 10

    # noinspection PyPep8Naming
    @aenum.skip
    class lcd_lock_active(aenum.Enum):
        pass

    LCD_LOCK_ACTIVE = 11

    # noinspection PyPep8Naming
    @aenum.skip
    class camera_locate_active(aenum.Enum):
        IS_ACTIVE = 1
        IS_NOT_ACTIVE = 0

    CAMERA_LOCATE_ACTIVE = 45

    # noinspection PyPep8Naming
    @aenum.skip
    class current_time_msec(aenum.Enum):
        pass

    CURRENT_TIME_MSEC = 57

    # noinspection PyPep8Naming
    @aenum.skip
    class next_poll_msec(aenum.Enum):
        pass

    NEXT_POLL_MSEC = 60

    # noinspection PyPep8Naming
    @aenum.skip
    class analytics_ready(aenum.Enum):
        # TODO: EXPERIMENTAL: ANALYTICS READY
        READY = 2
        NOT_READY = 0

    ANALYTICS_READY = 61

    # noinspection PyPep8Naming
    @aenum.skip
    class analytics_size(aenum.Enum):
        pass

    ANALYTICS_SIZE = 62

    # noinspection PyPep8Naming
    @aenum.skip
    class in_contextual_menu(aenum.Enum):
        IN_CONTEXT_MENU = 1
        NOT_IN_CONTEXT_MENU = 0

    IN_CONTEXTUAL_MENU = 63


# App
class App(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class mode(aenum.Enum):
        VIDEO = 0
        PHOTO = 1
        MULTISHOT = 2

        PLAYBACK = 4
        SETUP = 5
        CUTTING = 9  # Cut clip in playback menu, active while saving the clip

    MODE = 43

    # noinspection PyPep8Naming
    @aenum.skip
    class sub_mode(aenum.Enum):
        # Enum returns on search by value only the first found
        # => Introducing generic results

        FIRST_SUB_MODE = 0
        SECOND_SUB_MODE = 1
        THIRD_SUB_MODE = 2
        FORTH_SUB_MODE = 3

        VIDEO = 0
        SINGLE_PIC = 0
        BURST = 0

        TIMELAPSE_VIDEO = 1
        CONTINUOUS = 1
        TIMELAPSE = 1

        VIDEO_PHOTO = 2
        NIGHT_PHOTO = 2
        NIGHTLAPSE = 2

        LOOPING = 3

    SUB_MODE = 44


# Video
class Video(aenum.Enum):
    # Seconds, how long the current, ongoing video recording is
    VIDEO_PROGRESS_COUNTER = 13

    # noinspection PyPep8Naming
    @aenum.skip
    class video_protune_default(aenum.Enum):
        # Indicates if the video protune settings are different from the default ones
        IS_DEFAULT = 1
        IS_NOT_DEFAULT = 0

    VIDEO_PROTUNE_DEFAULT = 46


# Photo
class Photo(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class photo_protune_default(aenum.Enum):
        # Indicates if the photo protune settings are different from the default ones
        IS_DEFAULT = 1
        IS_NOT_DEFAULT = 0

    PHOTO_PROTUNE_DEFAULT = 47


# Multishot
class MultiShot(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class multi_shot_protune_default(aenum.Enum):
        # Indicates if the multi shot protune settings are different from the default ones
        IS_DEFAULT = 1
        IS_NOT_DEFAULT = 0

    MULTI_SHOT_PROTUNE_DEFAULT = 48

    # Seconds until next multishot photo will be taken (timelapse/nightlapse only?)
    MULTI_SHOT_COUNT_DOWN = 49


# Broadcast
class Broadcast(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class broadcast_progress_counter(aenum.Enum):
        pass

    BROADCAST_PROGRESS_COUNTER = 14

    # noinspection PyPep8Naming
    @aenum.skip
    class broadcast_viewer_count(aenum.Enum):
        pass

    BROADCAST_VIEWER_COUNT = 15

    # noinspection PyPep8Naming
    @aenum.skip
    class broadcast_bstatus(aenum.Enum):
        pass

    BROADCAST_BSTATUS = 16


# Wireless
class Wireless(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class enable(aenum.Enum):
        ENABLED = 1
        DISABLED = 0

    ENABLE = 17

    # noinspection PyPep8Naming
    @aenum.skip
    class pair_state(aenum.Enum):
        # TODO: EXPERIMENTAL: PAIR STATE
        pass

    PAIR_STATE = 19

    # noinspection PyPep8Naming
    @aenum.skip
    class pair_type(aenum.Enum):
        # TODO: EXPERIMENTAL: PAIR TYPE
        APP = 1
        REMOTE = 2

    PAIR_TYPE = 20

    # noinspection PyPep8Naming
    @aenum.skip
    class pair_time(aenum.Enum):
        pass

    PAIR_TIME = 21

    # noinspection PyPep8Naming
    @aenum.skip
    class scan_state(aenum.Enum):
        pass

    SCAN_STATE = 22

    # noinspection PyPep8Naming
    @aenum.skip
    class scan_time_msec(aenum.Enum):
        pass

    SCAN_TIME_MSEC = 23

    # noinspection PyPep8Naming
    @aenum.skip
    class pairing(aenum.Enum):
        pass

    PAIRING = 28

    # noinspection PyPep8Naming
    @aenum.skip
    class remote_control_version(aenum.Enum):
        pass

    REMOTE_CONTROL_VERSION = 26

    # noinspection PyPep8Naming
    @aenum.skip
    class remote_control_connected(aenum.Enum):
        pass

    REMOTE_CONTROL_CONNECTED = 27

    # noinspection PyPep8Naming
    @aenum.skip
    class app_count(aenum.Enum):
        pass

    APP_COUNT = 31

    # noinspection PyPep8Naming
    @aenum.skip
    class provision_status(aenum.Enum):
        pass

    PROVISION_STATUS = 24

    # noinspection PyPep8Naming
    @aenum.skip
    class wlan_ssid(aenum.Enum):
        pass

    WLAN_SSID = 29

    # noinspection PyPep8Naming
    @aenum.skip
    class ap_ssid(aenum.Enum):
        pass

    AP_SSID = 30

    # noinspection PyPep8Naming
    @aenum.skip
    class wifi_bars(aenum.Enum):
        pass

    WIFI_BARS = 56


# Stream
class Stream(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class enable(aenum.Enum):
        ENABLED = 1
        DISABLED = 0

    ENABLE = 32

    # noinspection PyPep8Naming
    @aenum.skip
    class supported(aenum.Enum):
        SUPPORTED = 1
        NOT_SUPPORTED = 0

    SUPPORTED = 55


# Storage
class Storage(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class sd_status(aenum.Enum):
        pass

    SD_STATUS = 33

    REMAINING_PHOTOS = 34

    REMAINING_VIDEO_TIME = 35

    REMAINING_SPACE = 54

    NUM_GROUP_PHOTOS = 36

    NUM_GROUP_VIDEO = 37

    NUM_TOTAL_PHOTOS = 38

    NUM_TOTAL_VIDEOS = 39

    NUM_HILIGHTS = 58

    LAST_HILIGHT_TIME_MSEC = 59

    REMAINING_TIMELAPSE_TIME = 64


# Setup
class Setup(aenum.Enum):
    DATE_TIME = 40


# FwUpdate
class FwUpdate(aenum.Enum):
    # noinspection PyPep8Naming
    @aenum.skip
    class ota_status(aenum.Enum):
        pass

    OTA_STATUS = 41

    # noinspection PyPep8Naming
    @aenum.skip
    class download_cancel_request_pending(aenum.Enum):
        pass

    DOWNLOAD_CANCEL_REQUEST_PENDING = 42


if __name__ == '__main__':
    for key in [App.mode.CUTTING, App.sub_mode]:
        try:
            print(reverse_lookup(key))
        except enum_exceptions.KeyNotFoundException as e:
            print(e)
    exit()

    key = None
    value = None
    try:
        a = FwUpdate.ota_status.TEST0
        _, b = lookup(41, 0)
        if a == b:
            print('yes')
        key, value = lookup(41, 0)
        print(key)
        print(value)
    except enum_exceptions.ValueForExistingKeyNotFoundException as e:
        print(key)
        print(e)
