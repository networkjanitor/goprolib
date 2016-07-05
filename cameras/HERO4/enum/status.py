import enum
import inspect


class KeyNotFoundException(Exception):
    def __init__(self, search_key, message='No information could be found for key {key}'):
        # Call the base class constructor with the parameters it needs
        message.format(key=search_key)
        super(KeyNotFoundException, self).__init__(message)

        # Custom values
        self.search_key = search_key


class ValueForExistingKeyNotFoundException(Exception):
    # the name is terrible, BUT it is descriptive
    def __init__(self, search_key, search_value, found_key, message='No value information could be found for key {key} and value {value}'):
        message.format(key=search_key, value=search_value)
        # Call the base class constructor with the parameters it needs
        super(ValueForExistingKeyNotFoundException, self).__init__(message)

        # Custom values
        self.search_key = search_key
        self.search_value = search_value
        self.found_key = found_key


class Status:
    """
    How keys and values are structured:

    Keys are found in different enum.Enum derived classes inside of the 'Status' class.
    All keys need to be named in uppercase letters.

    For each key there can be a value class (again, enum.Enum derived). This value class needs to be inside the class
    the key was found in. Furthermore the name of the value-class need to be lower case. In the future this should be
    changed to CamelCase, but I did not found a reliable snake_case to CamelCase converter in time.Feel free to add one.

    To make a search for a key or a key-value pair use the method lookup.
    """
    @staticmethod
    def lookup(key, value=None):
        # Search in all classes inside of 'Status' class
        for found_key_class in inspect.getmembers(Status, predicate=inspect.isclass):
            try:
                # Try to find key in class
                # If key is not found in the class, it raises an exception which starts the search in the next class
                key_lookup = Status._find(key, found_key_class[1])

                # Key found
                if value is not None:
                    # Key and value requested

                    # Search for the class which has the key name as class name (lower case)
                    # The can only be one class with the name
                    found_value_class = inspect.getmembers(Status.Wireless, predicate=lambda elem:
                                                            Status._nested_predicate(elem, key_lookup.name.lower()))
                    try:
                        value_lookup = Status._find(value, found_value_class[0][1].value)
                        # If such class exists and the value is found within it, return results for key and value
                        return key_lookup, value_lookup
                    except Exception as e:
                        # If such class exists, but the value is not found within it, catch exception and join case
                        # together with the case that no such class exists
                        pass
                    # No such class exists, raise exception with the found result for the key
                    raise ValueForExistingKeyNotFoundException(key_lookup)
                else:
                    # Only key requested
                    return key_lookup
            except KeyNotFoundException as e:
                # The key way not found in this class, catch exception and proceed to next class
                pass
        # Key was not found in any classes inside of 'Status' class, raise exception
        raise KeyNotFoundException(search_key=key)

    @staticmethod
    def _find(key, searchenum):
        try:
            for item in list(searchenum):
                if key == item.value:
                    return item
        except Exception:
            pass
        raise KeyNotFoundException(search_key=key)

    @staticmethod
    def _nested_predicate(elem, name):
        try:
            if elem is not None and elem.name == name:
                return True
        except:
            pass
        return False
    
    # System
    class System(enum.Enum):
        # noinspection PyPep8Naming
        class internal_battery_present(enum.Enum):
            pass
        INTERNAL_BATTERY_PRESENT = 1
        
        # noinspection PyPep8Naming
        class internal_battery_level(enum.Enum):
            pass
        INTERNAL_BATTERY_LEVEL = 2
        
        # noinspection PyPep8Naming
        class external_battery_present(enum.Enum):
            pass
        EXTERNAL_BATTERY_PRESENT = 3

        # noinspection PyPep8Naming
        class external_battery_level(enum.Enum):
            pass
        EXTERNAL_BATTERY_LEVEL = 4

        # noinspection PyPep8Naming
        class system_hot(enum.Enum):
            pass
        SYSTEM_HOT = 6

        # noinspection PyPep8Naming
        class system_busy(enum.Enum):
            pass
        SYSTEM_BUSY = 8

        # noinspection PyPep8Naming
        class quick_capture_active(enum.Enum):
            pass
        QUICK_CAPTURE_ACTIVE = 9

        # noinspection PyPep8Naming
        class encoding_active(enum.Enum):
            pass
        ENCODING_ACTIVE = 10

        # noinspection PyPep8Naming
        class lcd_lock_active(enum.Enum):
            pass
        LCD_LOCK_ACTIVE = 11

        # noinspection PyPep8Naming
        class camera_locate_active(enum.Enum):
            pass
        CAMERA_LOCATE_ACTIVE = 45

        # noinspection PyPep8Naming
        class current_time_msec(enum.Enum):
            pass
        CURRENT_TIME_MSEC = 57

        # noinspection PyPep8Naming
        class next_poll_msec(enum.Enum):
            pass
        NEXT_POLL_MSEC = 60

        # noinspection PyPep8Naming
        class analytics_ready(enum.Enum):
            pass
        ANALYTICS_READY = 61

        # noinspection PyPep8Naming
        class analytics_size(enum.Enum):
            pass
        ANALYTICS_SIZE = 62

        # noinspection PyPep8Naming
        class in_contextual_menu(enum.Enum):
            pass
        IN_CONTEXTUAL_MENU = 63

    # App
    class App(enum.Enum):
        # noinspection PyPep8Naming
        class mode(enum.Enum):
            pass
        MODE = 43

        # noinspection PyPep8Naming
        class sub_mode(enum.Enum):
            pass
        SUB_MODE = 44

    # Video
    class Video(enum.Enum):
        # noinspection PyPep8Naming
        class video_progress_counter(enum.Enum):
            pass
        VIDEO_PROGRESS_COUNTER = 13

        # noinspection PyPep8Naming
        class video_protune_default(enum.Enum):
            pass
        VIDEO_PROTUNE_DEFAULT = 46

    # Photo
    class Photo(enum.Enum):
        # noinspection PyPep8Naming
        class photo_protune_default(enum.Enum):
            pass
        PHOTO_PROTUNE_DEFAULT = 47

    # Multishot
    class MultiShot(enum.Enum):
        # noinspection PyPep8Naming
        class multi_shot_protune_default(enum.Enum):
            pass
        MULTI_SHOT_PROTUNE_DEFAULT = 48

        # noinspection PyPep8Naming
        class multi_shot_count_down(enum.Enum):
            pass
        MULTI_SHOT_COUNT_DOWN = 49

    # Broadcast
    class Broadcast(enum.Enum):
        # noinspection PyPep8Naming
        class broadcast_progress_counter(enum.Enum):
            pass
        BROADCAST_PROGRESS_COUNTER = 14

        # noinspection PyPep8Naming
        class broadcast_viewer_count(enum.Enum):
            pass
        BROADCAST_VIEWER_COUNT = 15

        # noinspection PyPep8Naming
        class broadcast_bstatus(enum.Enum):
            pass
        BROADCAST_BSTATUS = 16

    # Wireless
    class Wireless(enum.Enum):
        # noinspection PyPep8Naming
        class enable(enum.Enum):
            pass
        ENABLE = 17

        # noinspection PyPep8Naming
        class pair_state (enum.Enum):
            pass
        PAIR_STATE = 19

        # noinspection PyPep8Naming
        class pair_type(enum.Enum):
            pass
        PAIR_TYPE = 20

        # noinspection PyPep8Naming
        class pair_time(enum.Enum):
            pass
        PAIR_TIME = 21

        # noinspection PyPep8Naming
        class scan_state(enum.Enum):
            pass
        SCAN_STATE = 22

        # noinspection PyPep8Naming
        class scan_time_msec(enum.Enum):
            pass
        SCAN_TIME_MSEC = 23

        # noinspection PyPep8Naming
        class pairing(enum.Enum):
            pass
        PAIRING = 28

        # noinspection PyPep8Naming
        class remote_control_version(enum.Enum):
            pass
        REMOTE_CONTROL_VERSION = 26

        # noinspection PyPep8Naming
        class remote_control_connected(enum.Enum):
            pass
        REMOTE_CONTROL_CONNECTED = 27

        # noinspection PyPep8Naming
        class app_count(enum.Enum):
            pass
        APP_COUNT = 31

        # noinspection PyPep8Naming
        class provision_status(enum.Enum):
            pass
        PROVISION_STATUS = 24

        # noinspection PyPep8Naming
        class wlan_ssid(enum.Enum):
            pass
        WLAN_SSID = 29

        # noinspection PyPep8Naming
        class ap_ssid(enum.Enum):
            pass
        AP_SSID = 30

        # noinspection PyPep8Naming
        class wifi_bars(enum.Enum):
            pass
        WIFI_BARS = 56

    # Stream
    class Stream(enum.Enum):
        # noinspection PyPep8Naming
        class enable(enum.Enum):
            ENABLED = 1
            DISABLED = 0
        ENABLE = 32

        # noinspection PyPep8Naming
        class supported(enum.Enum):
            SUPPORTED = 1
            NOT_SUPPORTED = 0
        SUPPORTED = 55

    # Storage
    class Storage(enum.Enum):
        # noinspection PyPep8Naming
        class sd_status(enum.Enum):
            pass
        SD_STATUS = 33

        # noinspection PyPep8Naming
        class remaining_photos(enum.Enum):
            pass
        REMAINING_PHOTOS = 34

        # noinspection PyPep8Naming
        class remaining_video_time(enum.Enum):
            pass
        REMAINING_VIDEO_TIME = 35

        # noinspection PyPep8Naming
        class remaining_space(enum.Enum):
            pass
        REMAINING_SPACE = 54

        # noinspection PyPep8Naming
        class num_group_photos(enum.Enum):
            pass
        NUM_GROUP_PHOTOS = 36

        # noinspection PyPep8Naming
        class num_group_video(enum.Enum):
            pass
        NUM_GROUP_VIDEO = 37

        # noinspection PyPep8Naming
        class num_total_photos(enum.Enum):
            pass
        NUM_TOTAL_PHOTOS = 38

        # noinspection PyPep8Naming
        class num_total_videos(enum.Enum):
            pass
        NUM_TOTAL_VIDEOS = 39

        # noinspection PyPep8Naming
        class num_hilights(enum.Enum):
            pass
        NUM_HILIGHTS = 58

        # noinspection PyPep8Naming
        class last_hilight_time_msec(enum.Enum):
            pass
        LAST_HILIGHT_TIME_MSEC = 59

        # noinspection PyPep8Naming
        class remaining_timelapse_time(enum.Enum):
            pass
        REMAINING_TIMELAPSE_TIME = 64

    # Setup
    class Setup(enum.Enum):
        # noinspection PyPep8Naming
        class date_time(enum.Enum):
            pass
        DATE_TIME = 40

    # FwUpdate
    class FwUpdate(enum.Enum):
        # noinspection PyPep8Naming
        class ota_status(enum.Enum):
            pass
        OTA_STATUS = 41

        # noinspection PyPep8Naming
        class download_cancel_request_pending(enum.Enum):
            pass
        DOWNLOAD_CANCEL_REQUEST_PENDING = 42


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


if __name__ == '__main__':
    key = None
    value = None
    try:
        key, value = Status.lookup(19, 0)
        print(key)
        print(value)
    except ValueForExistingKeyNotFoundException as e:
        print(key)
        print(e)
