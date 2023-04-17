from enum import Enum, auto
''' Цей код містить визначення двох класів перерахувань (enumeration classes): "SideType" та "CheckerType". '''
class SideType(Enum): 
    WHITE = auto() # перерахування: "WHITE"
    BLACK = auto() # перерахування: "BLACK"
    ''' Ці перерахування представляють сторони гравців у грі. Для того, щоб отримати протилежну сторону, 
    використовується метод "opposite", який приймає один параметр "side" (сторону) та повертає протилежну сторону.'''
    def opposite(side):
        if (side == SideType.WHITE):
            return SideType.BLACK
        elif (side == SideType.BLACK):
            return SideType.WHITE
        else: raise ValueError()
'''Клас "CheckerType" також містить чотири перерахування: "NONE", "WHITE_REGULAR", "BLACK_REGULAR", "WHITE_QUEEN" та 
"BLACK_QUEEN". Ці перерахування відображають типи шашок, які можуть бути на дошці.'''
class CheckerType(Enum):
    NONE = auto() # "NONE" використовується для позначення пустої клітинки на дошці.
    WHITE_REGULAR = auto() # "WHITE_REGULAR" відображає звичайні білі шашки.
    BLACK_REGULAR = auto() # "BLACK_REGULAR" відображає звичайні чорні шашки.
    WHITE_QUEEN = auto() # "WHITE_QUEEN" відображає білу дамку.
    BLACK_QUEEN = auto() # "BLACK_QUEEN" відображає чорну дамку.