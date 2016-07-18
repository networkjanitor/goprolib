import aenum

# Fisheye
class Fisheye(aenum.Enum):
    WIDE_4x3 = [0.06335, -0.18432, -0.13009] # magic https://www.imagemagick.org/Usage/lens/
    #WIDE_4x3 = [0.0944, -0.1226, -0.1492] # wrong
    #MEDIUM_4x3 = [0.0722, -0.0944, -0.1157]
    #NARROW_4x3 = [0.0491, -0.0646, -0.0797]

    #WIDE_16x9 = [0.0695, -0.1182, -0.1336]
    #MEDIUM_16x9 = [0.055, -0.0944, -0.1071]
    #NARROW_16x9 = [0.0372, -0.0644, -0.0736]


if __name__ == '__main__':
    x = Fisheye.WIDE_4x3
    print(x.value)