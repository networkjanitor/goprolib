import enum




class VideoResolution(enum.Enum):
    R4K_SUPER_VIEW = 2
    R4K = 1
    R2_7K_SUPER_VIEW = 5
    R2_7K = 4
    R2_7K_4_3 = 6
    R1440 = 7
    R1080_SuperView = 8
    R1080 = 9
    R960 = 10
    R720_SuperView = 11
    R720 = 11
    WVGA = 13


class HERO4:
    def __init__(self):
        print(VideoResolution(11))
        for key in VideoResolution:
            print(key)
            print(key.value)
            print('###')

if __name__ == '__main__':
    h4 = HERO4()