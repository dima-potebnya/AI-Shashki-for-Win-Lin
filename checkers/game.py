from tkinter import Canvas, Event, messagebox
from PIL import Image, ImageTk
from random import choice
from pathlib import Path
from time import sleep
from math import inf
from pygame import mixer

from checkers.field import Field
from checkers.move import Move
from checkers.constants import *
from checkers.enums import CheckerType, SideType

class Game:
    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int, cell_size: int, only_table: bool, PLAY_WITH: str, PLAYER_SIDE: SideType, ANIMATION_SPEED: int, MAX_PREDICTION_DEPTH: int):
        self.__canvas = canvas
        self.cell_size = cell_size
        self.__field = Field(x_field_size, y_field_size)
        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()
        self.PLAY_WITH = PLAY_WITH
        self.PLAYER_SIDE = PLAYER_SIDE
        self.PLAYER2_SIDE = PLAYER_SIDE
        self.ANIMATION_SPEED = ANIMATION_SPEED
        self.MAX_PREDICTION_DEPTH = MAX_PREDICTION_DEPTH
        self.FIELD_COLORS = FIELD_COLORS
        self.NUM_OF_THEME = '1'
        self.somebody_win = False
        self.PLAY_SOUND = True
        mixer.init() # Ініціалізація міксеру для подальшого використання звукового модулю
        if(self.PLAYER_SIDE==SideType.WHITE): self.PLAYER2_SIDE = SideType.BLACK
        if(self.PLAYER_SIDE==SideType.BLACK): self.PLAYER2_SIDE = SideType.WHITE
        if (self.PLAY_WITH == "HUMAN"): self.__player_turn = self.PLAYER_SIDE
        if (self.PLAY_WITH == "AI"): self.__player_turn = True
        if (self.PLAY_WITH == "HUMAN"): self.is_running = False # Булева змінна перевірки натискання миші
        if only_table: 
            self.__draw_field_grid(self.FIELD_COLORS)
            return
        self.__init_images()
        self.__draw()

        # Если игрок играет за чёрных, то совершить ход противника
        if (self.PLAYER_SIDE == SideType.BLACK and self.PLAY_WITH == "AI"):
            self.__handle_enemy_turn()

    def __init_images(self):
        '''Инициализация изображений'''
        self.__images = {
            CheckerType.WHITE_REGULAR: ImageTk.PhotoImage(Image.open(Path('assets/theme'+self.NUM_OF_THEME, 'white.png')).resize((self.cell_size, self.cell_size), Image.ANTIALIAS)),
            CheckerType.BLACK_REGULAR: ImageTk.PhotoImage(Image.open(Path('assets/theme'+self.NUM_OF_THEME, 'black.png')).resize((self.cell_size, self.cell_size), Image.ANTIALIAS)),
            CheckerType.WHITE_QUEEN: ImageTk.PhotoImage(Image.open(Path('assets/theme'+self.NUM_OF_THEME, 'white-queen.png')).resize((self.cell_size, self.cell_size), Image.ANTIALIAS)),
            CheckerType.BLACK_QUEEN: ImageTk.PhotoImage(Image.open(Path('assets/theme'+self.NUM_OF_THEME, 'black-queen.png')).resize((self.cell_size, self.cell_size), Image.ANTIALIAS)),
        }

    def __animate_move(self, move: Move):
        '''Анимация перемещения шашки'''
        self.__animated_cell = Point(move.from_x, move.from_y)
        self.__draw()

        # Програвання звуку переміщення шашки 
        self.__play_music("make_step.mp3")

        # Создание шашки для анимации
        animated_checker = self.__canvas.create_image(move.from_x * self.cell_size, move.from_y * self.cell_size, image=self.__images.get(self.__field.type_at(move.from_x, move.from_y)), anchor='nw', tag='animated_checker')
        
        # Вектора движения
        dx = 1 if move.from_x < move.to_x else -1
        dy = 1 if move.from_y < move.to_y else -1

        # Анимация
        for distance in range(abs(move.from_x - move.to_x)):
            for _ in range(100 // self.ANIMATION_SPEED):
                self.__canvas.move(animated_checker, self.ANIMATION_SPEED / 100 * self.cell_size * dx, self.ANIMATION_SPEED / 100 * self.cell_size * dy)
                self.__canvas.update()
                sleep(0.01)
        self.__animated_cell = Point()
    # функція для зміни теми в процесі гри
    def ch_theme(self, NO_GAME, NUM_OF_THEME): # вхідні параметри наявності гри та номера теми
        if NUM_OF_THEME == 1:
            self.FIELD_COLORS = ['#DCB255', '#613416'] # ставимо кольори поля однаковими для всього класу
        if NUM_OF_THEME == 2:
            self.FIELD_COLORS = ['#D39E58', '#9D5D16'] # ставимо кольори поля однаковими для всього класу 
        if NUM_OF_THEME == 3:
            self.FIELD_COLORS = ['#E7CFA9', '#927456'] # ставимо кольори поля однаковими для всього класу
        self.NUM_OF_THEME = str(NUM_OF_THEME)
        if NO_GAME == False: # якщо нова гра натиснута то відрисовуємо все
            self.__init_images()
            self.__draw()

    def off_on_sounds(self, SOUND_ON_OFF):
        self.PLAY_SOUND = SOUND_ON_OFF

    def __play_music(self,type_of_music):
        if self.PLAY_SOUND: # якщо дозвіл на музику дали то
            # завантаження звукового файлу
            sound = mixer.Sound("assets/sounds/"+type_of_music)
            # вмикається звуковий файл на програвання
            sound.play()

    def __draw(self):
        '''Відрисовка сітки поля та шашок'''
        self.__canvas.delete('all')
        self.__draw_field_grid(self.FIELD_COLORS)
        self.__draw_checkers()

    def __draw_field_grid(self, FIELD_COLORS):
        '''Відрисовка сітки поля'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                self.__canvas.create_rectangle(x * self.cell_size, y * self.cell_size, x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size, fill=self.FIELD_COLORS[(y + x) % 2], width=0, tag='boards')

                # Відрисовка рамок в необхідних клітинах
                if (x == self.__selected_cell.x and y == self.__selected_cell.y):
                    self.__canvas.create_rectangle(x * self.cell_size + BORDER_WIDTH // 2, y * self.cell_size + BORDER_WIDTH // 2, x * self.cell_size + self.cell_size - BORDER_WIDTH // 2, y * self.cell_size + self.cell_size - BORDER_WIDTH // 2, outline=SELECT_BORDER_COLOR, width=BORDER_WIDTH, tag='border')
                elif (x == self.__hovered_cell.x and y == self.__hovered_cell.y):
                    self.__canvas.create_rectangle(x * self.cell_size + BORDER_WIDTH // 2, y * self.cell_size + BORDER_WIDTH // 2, x * self.cell_size + self.cell_size - BORDER_WIDTH // 2, y * self.cell_size + self.cell_size - BORDER_WIDTH // 2, outline=HOVER_BORDER_COLOR,  width=BORDER_WIDTH, tag='border')
                
                # Відрисовка можливих точок переміщення, якщо є обрана комірка
                if (self.__selected_cell): 
                    if (self.PLAY_WITH == "AI"): player_moves_list = self.__get_moves_list(self.PLAYER_SIDE)
                    if (self.PLAY_WITH == "HUMAN"): player_moves_list = self.__get_moves_list(self.__player_turn)
                    for move in player_moves_list:
                        if (self.__selected_cell.x == move.from_x and self.__selected_cell.y == move.from_y):
                            self.__canvas.create_oval(move.to_x * self.cell_size + self.cell_size / 3, move.to_y * self.cell_size + self.cell_size / 3, move.to_x * self.cell_size + (self.cell_size - self.cell_size / 3), move.to_y * self.cell_size + (self.cell_size - self.cell_size / 3), fill=POSIBLE_MOVE_CIRCLE_COLOR, width=0, tag='posible_move_circle' )

    def __draw_checkers(self):
        '''Відрисовка шашок'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Не отрисовывать пустые ячейки и анимируемую шашку
                if (self.__field.type_at(x, y) != CheckerType.NONE and not (x == self.__animated_cell.x and y == self.__animated_cell.y)):
                    self.__canvas.create_image(x * self.cell_size, y * self.cell_size, image=self.__images.get(self.__field.type_at(x, y)), anchor='nw', tag='checkers')

    def mouse_move(self, event: Event):
        '''Событие перемещения мышки'''
        x, y = (event.x) // self.cell_size, (event.y) // self.cell_size
        if (x != self.__hovered_cell.x or y != self.__hovered_cell.y):
            self.__hovered_cell = Point(x, y)

            # Якщо хід гравця та мишкою не нажимають, то перерисувати
            if (self.PLAY_WITH == "HUMAN"):
                if (self.__player_turn and not self.is_running): self.__draw() 
            if (self.PLAY_WITH == "AI"): 
                if (self.__player_turn): self.__draw()

    def mouse_down(self, event: Event):
        '''Событие нажатия мышки'''
        if not (self.__player_turn): return 
        if (self.somebody_win): return # якщо хтось переміг то вихід з функції
        if (self.PLAY_WITH == "HUMAN"):
            if (self.is_running): return # Якщо мишка нажата то вихід з функції
            self.is_running = True # Натискання мишею починаються
        x, y = (event.x) // self.cell_size, (event.y) // self.cell_size

        # Если точка не внутри поля
        if not (self.__field.is_within(x, y)): return
              
        if (self.PLAY_WITH == "HUMAN"):
            if (self.__player_turn == SideType.WHITE):
                player_checkers = WHITE_CHECKERS
            elif (self.__player_turn == SideType.BLACK):
                player_checkers = BLACK_CHECKERS
            else: return
        
        if (self.PLAY_WITH == "AI"):
            if (self.PLAYER_SIDE == SideType.WHITE):
                player_checkers = WHITE_CHECKERS
            elif (self.PLAYER_SIDE == SideType.BLACK):
                player_checkers = BLACK_CHECKERS
            else: return

        # Если нажатие по шашке игрока, то выбрать её
        if (self.__field.type_at(x, y) in player_checkers):
            self.__selected_cell = Point(x, y)
            self.__draw()
            # Програвання звуку по натисканню мишки 
            self.__play_music("pressed_on_checker.mp3")
        elif (self.__player_turn):
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)

            # Если нажатие по ячейке, на которую можно походить
            if (self.PLAY_WITH == "HUMAN"):
                if (move in self.__get_moves_list(self.__player_turn)):
                    self.__handle_player_turn(move)
            # Если нажатие по ячейке, на которую можно походить
            if (self.PLAY_WITH == "AI"):
                if (move in self.__get_moves_list(self.PLAYER_SIDE)):
                    self.__handle_player_turn(move)
                
                # Если не ход игрока, то ход противника
                if not (self.__player_turn):
                    self.__handle_enemy_turn()
        if (self.PLAY_WITH == "HUMAN"): self.is_running = False # Натискання мишею закінчуються

    def __handle_move(self, move: Move, draw: bool = True) -> bool:
        '''Совершение хода'''
        if (draw): self.__animate_move(move)

        # Изменение типа шашки, если она дошла до края
        if (move.to_y == 0 and self.__field.type_at(move.from_x, move.from_y) == CheckerType.WHITE_REGULAR):
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.WHITE_QUEEN)
        elif (move.to_y == self.__field.y_size - 1 and self.__field.type_at(move.from_x, move.from_y) == CheckerType.BLACK_REGULAR):
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.BLACK_QUEEN)
            
        # Изменение позиции шашки
        self.__field.at(move.to_x, move.to_y).change_type(self.__field.type_at(move.from_x, move.from_y))
        self.__field.at(move.from_x, move.from_y).change_type(CheckerType.NONE)

        # Вектора движения
        dx = -1 if move.from_x < move.to_x else 1
        dy = -1 if move.from_y < move.to_y else 1

        # Удаление съеденных шашек
        has_killed_checker = False
        
        x, y = move.to_x, move.to_y
        while (x != move.from_x or y != move.from_y):
            x += dx
            y += dy
            if (self.__field.type_at(x, y) != CheckerType.NONE):
                self.__field.at(x, y).change_type(CheckerType.NONE)
                has_killed_checker = True
        if (draw): self.__draw()
        return has_killed_checker

    def __handle_player_turn(self, move: Move):
        '''Обработка хода игрока'''
        # Была ли убита шашка
        if (self.PLAY_WITH == "AI"): self.__player_turn = False
        has_killed_checker = self.__handle_move(move)
        if (self.PLAY_WITH == "HUMAN"):
            required_moves_list = list(filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y, self.__get_required_moves_list(self.__player_turn)))
        if (self.PLAY_WITH == "AI"):
            required_moves_list = list(filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y, self.__get_required_moves_list(self.PLAYER_SIDE)))
        # Если есть ещё ход этой же шашкой
        if (self.PLAY_WITH == "AI"):
            if (has_killed_checker and required_moves_list ):
                self.__player_turn = True
        # Если есть ещё ход этой же шашкой
        if (self.PLAY_WITH == "HUMAN"):
            if (has_killed_checker and required_moves_list):
            # Оставляем текущего игрока, чтобы он сделал еще один ход
                pass
            else:
            # Меняем игрока, чтобы следующий сделал ход
                if self.__player_turn == self.PLAYER_SIDE:
                    self.__player_turn = self.PLAYER2_SIDE
                else:
                    self.__player_turn = self.PLAYER_SIDE
                
        if (self.PLAY_WITH == "HUMAN"): self.__check_for_game_over()
        self.__selected_cell = Point()

    def __handle_enemy_turn(self):
        '''Обработка хода противника (компьютера)'''
        self.__player_turn = False

        optimal_moves_list = self.__predict_optimal_moves(SideType.opposite(self.PLAYER_SIDE))

        for move in optimal_moves_list:
            self.__handle_move(move)
            
        self.__player_turn = True
        
        self.__check_for_game_over()

    def __check_for_game_over(self):
        '''Перевірка на кінець гри'''
        white_moves_list = self.__get_moves_list(SideType.WHITE)
        black_moves_list = self.__get_moves_list(SideType.BLACK)
        if (self.PLAY_WITH == "HUMAN"):
            # Перевіряємо, чи є доступні ходи для поточного гравця
            if not white_moves_list:
                winner = "Чорні" if self.__player_turn == self.PLAYER_SIDE else "Білі"
                self.__play_music("winner.mp3") # Програвання звука перемоги 
                answer = messagebox.showinfo('Кінець гри', f'{winner} виграли')
            elif not black_moves_list:
                winner = "Білі" if self.__player_turn == self.PLAYER_SIDE else "Чорні"
                self.__play_music("winner.mp3") # Програвання звука перемоги 
                answer = messagebox.showinfo('Кінець гри', f'{winner} виграли')
        if self.PLAY_WITH == "AI":
            # Перевіряємо, чи є можливі ходи у білих та чорних шашок
            if not white_moves_list:
                # Білі програли
                side = SideType.BLACK
                message = 'Чорні виграли'
            elif not black_moves_list:
                # Чорні програли
                side = SideType.WHITE
                message = 'Білі виграли'
            else:
                return
    
            self.somebody_win = True
            # Вибір звука в залежності від переможеної сторони
            music_file = "winner.mp3" if side == self.PLAYER_SIDE else "loser.mp3"
            self.__play_music(music_file) # Програвання звука перемоги/програшу
            answer = messagebox.showinfo('Кінець гри', message)
 
    def __predict_optimal_moves(self, side: SideType) -> list[Move]:
        '''Предсказать оптимальный ход'''
        best_result = 0
        optimal_moves = []
        predicted_moves_list = self.__get_predicted_moves_list(side)

        if (predicted_moves_list):
            field_copy = Field.copy(self.__field)
            for moves in predicted_moves_list:
                for move in moves:
                    self.__handle_move(move, draw=False)

                try:
                    if (side == SideType.WHITE):
                        result = self.__field.white_score / self.__field.black_score
                    elif (side == SideType.BLACK):
                        result = self.__field.black_score / self.__field.white_score
                except ZeroDivisionError:
                        result = inf
                
                if (result > best_result):
                    best_result = result
                    optimal_moves.clear()
                    optimal_moves.append(moves)
                elif (result == best_result):
                    optimal_moves.append(moves)

                self.__field = Field.copy(field_copy)

        optimal_move = []
        if (optimal_moves):
            # Фильтрация хода
            for move in choice(optimal_moves):
                if   (side == SideType.WHITE and self.__field.type_at(move.from_x, move.from_y) in BLACK_CHECKERS): break
                elif (side == SideType.BLACK and self.__field.type_at(move.from_x, move.from_y) in WHITE_CHECKERS): break

                optimal_move.append(move)

        return optimal_move

    def __get_predicted_moves_list(self, side: SideType, current_prediction_depth: int = 0, all_moves_list: list[Move] = [], current_moves_list: list[Move] = [], required_moves_list: list[Move] = []) -> list[Move]:
        '''Предсказать все возможные ходы'''

        if (current_moves_list):
            all_moves_list.append(current_moves_list)
        else:
            all_moves_list.clear()

        if (required_moves_list):
            moves_list = required_moves_list
        else:
            moves_list = self.__get_moves_list(side)

        if (moves_list and current_prediction_depth < self.MAX_PREDICTION_DEPTH):
            field_copy = Field.copy(self.__field)
            for move in moves_list:
                has_killed_checker = self.__handle_move(move, draw=False)

                required_moves_list = list(filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y, self.__get_required_moves_list(side)))

                # Если есть ещё ход этой же шашкой
                if (has_killed_checker and required_moves_list):
                    self.__get_predicted_moves_list(side, current_prediction_depth, all_moves_list, current_moves_list + [move], required_moves_list)
                else:
                    self.__get_predicted_moves_list(SideType.opposite(side), current_prediction_depth + 1, all_moves_list, current_moves_list + [move])

                self.__field = Field.copy(field_copy)

        return all_moves_list

    def __get_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка ходов'''
        moves_list = self.__get_required_moves_list(side)
        if not (moves_list):
            moves_list = self.__get_optional_moves_list(side)
        return moves_list

    def __get_required_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка обязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if (side == SideType.WHITE):
            friendly_checkers = WHITE_CHECKERS
            enemy_checkers = BLACK_CHECKERS
        elif (side == SideType.BLACK):
            friendly_checkers = BLACK_CHECKERS
            enemy_checkers = WHITE_CHECKERS
        else: return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):

                # Для обычной шашки
                if (self.__field.type_at(x, y) == friendly_checkers[0]):
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        if self.__field.type_at(x + offset.x, y + offset.y) in enemy_checkers and self.__field.type_at(x + offset.x * 2, y + offset.y * 2) == CheckerType.NONE:
                            moves_list.append(Move(x, y, x + offset.x * 2, y + offset.y * 2))

                # Для дамки
                elif (self.__field.type_at(x, y) == friendly_checkers[1]):
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        has_enemy_checker_on_way = False

                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue

                            # Если на пути не было вражеской шашки
                            if (not has_enemy_checker_on_way):
                                if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in enemy_checkers):
                                    has_enemy_checker_on_way = True
                                    continue
                                # Если на пути союзная шашка - то закончить цикл
                                elif (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in friendly_checkers):
                                    break
                            
                            # Если на пути была вражеская шашка
                            if (has_enemy_checker_on_way):
                                if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE):
                                    moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                                else:
                                    break
                            
        return moves_list

    def __get_optional_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка необязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if (side == SideType.WHITE):
            friendly_checkers = WHITE_CHECKERS
        elif (side == SideType.BLACK):
            friendly_checkers = BLACK_CHECKERS
        else: return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Для обычной шашки
                if (self.__field.type_at(x, y) == friendly_checkers[0]):
                    for offset in MOVE_OFFSETS[:2] if side == SideType.WHITE else MOVE_OFFSETS[2:]:
                        if not (self.__field.is_within(x + offset.x, y + offset.y)): continue

                        if (self.__field.type_at(x + offset.x, y + offset.y) == CheckerType.NONE):
                            moves_list.append(Move(x, y, x + offset.x, y + offset.y))

                # Для дамки
                elif (self.__field.type_at(x, y) == friendly_checkers[1]):
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x, y + offset.y)): continue

                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue

                            if (self.__field.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE):
                                moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                            else:
                                break
        return moves_list