from aenum import Enum, skip

class enumA(Enum):
    @skip
    class enumb(Enum):
        elementA = 0
        elementB = 1
    ENUMB = 42
    @skip
    class enumc(Enum):
        elementC = 1
        elementD = 0
    ENUMC = 41

if __name__ == '__main__':
    print(enumA.ENUMB)
    print(enumA.enumb.elementA)