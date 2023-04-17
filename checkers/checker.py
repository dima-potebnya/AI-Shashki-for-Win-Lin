from checkers.enums import CheckerType

class Checker:
    #Конструктор класу приймає параметр type за замовчуванням зі значенням CheckerType.NONE (шашка без типу)
    def __init__(self, type: CheckerType = CheckerType.NONE):
        self.__type = type
    #Властивість type містить тип шашки (WHITE_REGULAR, BLACK_REGULAR, WHITE_QUEEN, BLACK_QUEEN або NONE).
    @property
    def type(self):
        return self.__type
    #Метод change_type приймає параметр type і змінює тип шашки.
    def change_type(self, type: CheckerType):
        self.__type = type