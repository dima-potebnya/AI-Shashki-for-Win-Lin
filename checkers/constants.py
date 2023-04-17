from checkers.point import Point
from checkers.enums import CheckerType, SideType

# З ким грати з людиною (HUMAN) або ж з комп'ютером (AI)
#PLAY_WITH = "AI"
# Сторона, за яку грає гравець
#PLAYER_SIDE = SideType.WHITE
# Розмір поля, 7-мал,8-звич,14-вел
#X_SIZE = Y_SIZE = 8
# Розмір комірки (у пікселях) 45-мал, 60-сер, 75-вел
#CELL_SIZE = 60
# Швидкість анімації (більше = швидше) 2-мал,4-сер,6-вел
#ANIMATION_SPEED = 4
# Кількість ходів для передбачення 1-мін, 6-макс
#MAX_PREDICTION_DEPTH = 1

# Ширина рамки (Бажано має бути парною)
BORDER_WIDTH = 2 * 2

# Кольори ігрової дошки
FIELD_COLORS = ['#DCB255', '#613416']
# Колір рамки при наведенні на комірку мишкою
HOVER_BORDER_COLOR = '#54b346'
# Колір рамки при виділенні комірки
SELECT_BORDER_COLOR = '#944444'
# Колір кружечків можливих ходів
POSIBLE_MOVE_CIRCLE_COLOR = '#944444'

# Можливі зсуви ходів шашок
MOVE_OFFSETS = [
    Point(-1, -1),
    Point( 1, -1),
    Point(-1,  1),
    Point( 1,  1)
]

# Масиви типів білих і чорних шашок [пішка, дамка]
WHITE_CHECKERS = [CheckerType.WHITE_REGULAR, CheckerType.WHITE_QUEEN]
BLACK_CHECKERS = [CheckerType.BLACK_REGULAR, CheckerType.BLACK_QUEEN]