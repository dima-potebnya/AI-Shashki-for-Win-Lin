from tkinter import Canvas, Frame, Button
from checkers.settings import Settings
from checkers.enums import CheckerType, SideType
from checkers.game import Game

class Buttons:
    def __init__(self, parent):
        self.parent = parent
        # З ким грати з людиною (HUMAN) або ж з комп'ютером (AI)
        self.PLAY_WITH = "AI"
        # Сторона, за яку грає гравець
        self.PLAYER_SIDE = SideType.BLACK
        # Розмір поля, 7-мал,8-звич,14-вел
        self.X_SIZE = self.Y_SIZE = 8
        # Розмір комірки (у пікселях) 45-мал, 60-сер, 75-вел
        self.CELL_SIZE = 60
        # Швидкість анімації (більше = швидше) 2-мал,4-сер,6-вел
        self.ANIMATION_SPEED = 4
        # Кількість ходів для передбачення 1-мін, 6-макс
        self.MAX_PREDICTION_DEPTH = 1
        self.NO_GAME = True
        self.count_theme = 2
        self.SOUND_ON = True
        # Создание холста
        self.canvas = Canvas(parent, width=self.CELL_SIZE * self.X_SIZE, height=self.CELL_SIZE * self.Y_SIZE)
        self.canvas.grid(row=1, column=0, padx=10, pady=10) 
        
        self.game = Game(self.canvas, self.X_SIZE, self.Y_SIZE, self.CELL_SIZE, True, self.PLAY_WITH, self.PLAYER_SIDE, self.ANIMATION_SPEED, self.MAX_PREDICTION_DEPTH)
        self.button_frame = Frame(parent)
        self.button_frame.grid(row=0, column=0, columnspan=5, pady=10)
        
        self.start_button = Button(self.button_frame, text="Почати гру", command=self.new_game)
        self.start_button.pack(side="left", padx=10)

        self.settings_button = Button(self.button_frame, text="Змінити тему", command=self.change_theme)
        self.settings_button.pack(side="left", padx=10)

        self.sound_button = Button(self.button_frame, text="Вимкнути звук", command=self.sound_on_off)
        self.sound_button.pack(side="left", padx=10)

        self.end_button = Button(self.button_frame, text="Закінчити гру", command=self.end_game)
        self.end_button.pack(side="left", padx=10)
    
    def new_game(self):
        self.NO_GAME = False
        settings = Settings(self.parent, self.canvas, self.PLAY_WITH, self.PLAYER_SIDE, self.X_SIZE, self.Y_SIZE, self.CELL_SIZE, self.ANIMATION_SPEED, self.MAX_PREDICTION_DEPTH)
        self.PLAY_WITH = settings.get_PLAY_WITH()
        self.PLAYER_SIDE = settings.get_PLAYER_SIDE()
        self.X_SIZE = settings.get_X_SIZE()
        self.Y_SIZE = settings.get_Y_SIZE()
        self.CELL_SIZE = settings.get_CELL_SIZE()
        self.ANIMATION_SPEED = settings.get_ANIMATION_SPEED()
        self.MAX_PREDICTION_DEPTH = settings.get_MAX_PREDICTION_DEPTH()
        print("Грати з ",self.PLAY_WITH,"\nКолір шашок ",
              self.PLAYER_SIDE,"\nРозмір поля ",self.X_SIZE,"х",self.Y_SIZE,
              "\nРозмір комірок",self.CELL_SIZE,"\nШвидкість анімації ",
              self.ANIMATION_SPEED,"\nВажкість ШІ ",self.MAX_PREDICTION_DEPTH,"\n")
        self.canvas = Canvas(self.parent, width=self.CELL_SIZE * self.X_SIZE, height=self.CELL_SIZE * self.Y_SIZE)
        self.canvas.grid(row=1, column=0, padx=10, pady=10)
        self.game = Game(self.canvas, self.X_SIZE, self.Y_SIZE, self.CELL_SIZE, False, self.PLAY_WITH, self.PLAYER_SIDE, self.ANIMATION_SPEED, self.MAX_PREDICTION_DEPTH)
        self.canvas.bind("<Motion>", self.game.mouse_move)
        self.canvas.bind("<Button-1>", self.game.mouse_down)

    def change_theme(self):
        if self.NO_GAME == False: # кнопка не реагує коли пусте поле
            self.game.ch_theme(self.NO_GAME,self.count_theme)    
            if self.count_theme == 3: self.count_theme = 0
            self.count_theme += 1
        
    def end_game(self):
        self.NO_GAME = True
        self.canvas.destroy()
        self.canvas = Canvas(self.parent, width=self.CELL_SIZE * self.X_SIZE, height=self.CELL_SIZE * self.Y_SIZE)
        self.canvas.grid(row=1, column=0, padx=10, pady=10)
        self.game = Game(self.canvas, self.X_SIZE, self.Y_SIZE, self.CELL_SIZE, True, self.PLAY_WITH, self.PLAYER_SIDE, self.ANIMATION_SPEED, self.MAX_PREDICTION_DEPTH)
    
    def sound_on_off(self):
        self.SOUND_ON = not self.SOUND_ON
        btntext="Вимкнути звук" if self.SOUND_ON else "Увімкнути звук"
        self.sound_button.configure(text=btntext)
        self.game.off_on_sounds(self.SOUND_ON)
        