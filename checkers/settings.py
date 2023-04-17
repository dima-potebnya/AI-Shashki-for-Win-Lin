from tkinter import PhotoImage
import tkinter as tk
import tkinter.font as tkFont
from checkers.enums import CheckerType, SideType

class Settings:
    def __init__(self,parent,canvas,PLAY_WITH,PLAYER_SIDE,X_SIZE,Y_SIZE,CELL_SIZE,ANIMATION_SPEED,MAX_PREDICTION_DEPTH):
        # Создание окна
        self.PLAY_WITH = PLAY_WITH
        self.PLAYER_SIDE = PLAYER_SIDE
        self.X_SIZE = X_SIZE
        self.Y_SIZE = Y_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.ANIMATION_SPEED = ANIMATION_SPEED
        self.MAX_PREDICTION_DEPTH = MAX_PREDICTION_DEPTH
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки гри")
        self.window.geometry("310x280")
        self.window.resizable(0, 0)
        self.window.iconphoto(False, PhotoImage(file='assets/set.png'))
        self.canvas = canvas
        # Шрифти
        self.myfont = tkFont.Font(family="Arial", size=12, weight="normal")
        self.create_values()
        self.window.mainloop()
        
    # Функция для обработки нажатия кнопки "OK"
    def ok_button_clicked(self):
        # Получение выбранных пользователем значений
        self.play_with = self.play_with_var.get()
        self.checker_color = self.checker_color_var.get()
        self.board_size = self.board_size_var.get()
        self.animation_speed = self.animation_speed_var.get()
        self.ai_difficulty = self.ai_difficulty_var.get()
        # Вывод выбранных пользователем значений в консоль
        if(self.play_with=="Інтелектом"):self.PLAY_WITH = "AI"
        if(self.play_with=="Людиною"):self.PLAY_WITH = "HUMAN"
        if(self.checker_color=="Білий"):self.PLAYER_SIDE = SideType.WHITE
        if(self.checker_color=="Чорний"):self.PLAYER_SIDE = SideType.BLACK
        if(self.board_size=="Маленький"):
            self.CELL_SIZE = 69
            self.X_SIZE = self.Y_SIZE = 7
        if(self.board_size=="Звичайний"):
            self.CELL_SIZE = 60
            self.X_SIZE = self.Y_SIZE = 8
        if(self.board_size=="Великий"):
            self.CELL_SIZE = 40
            self.X_SIZE = self.Y_SIZE = 12
        if(self.animation_speed=="Маленька"):self.ANIMATION_SPEED = 2
        if(self.animation_speed=="Середня"):self.ANIMATION_SPEED = 4
        if(self.animation_speed=="Велика"):self.ANIMATION_SPEED = 6
        if(self.ai_difficulty=="Слаба"):self.MAX_PREDICTION_DEPTH = 1
        if(self.ai_difficulty=="Середня"):self.MAX_PREDICTION_DEPTH = 3
        if(self.ai_difficulty=="Висока"):self.MAX_PREDICTION_DEPTH = 5
        # Закрытие окна
        self.canvas.destroy()
        self.window.destroy()
        self.window.quit()
        
    def set_menu(self,out:tk.StringVar,myfont:tkFont,col:int,row:int,py:int,px:int,val1:str,val2:str,val3:str):
        if val3==0:
            self.widget = tk.OptionMenu(self.window, out, val1, val2)
        else:
            self.widget = tk.OptionMenu(self.window, out, val1, val2, val3)
        self.widget.config(font=self.myfont) # Встановлюємо шрифт у віджет меню
        self.menu = self.window.nametowidget(self.widget.menuname)  # Отримуємо віджет меню
        self.menu.config(font=self.myfont)  # Встановлення шрифту випадаючого списку
        self.widget.grid(column=col, row=row, pady=py, padx=px)
        
    def set_label(self,text:str,myfont:tkFont,col:int,row:int,py:int,px:int):
        label = tk.Label(self.window, text=text, font=self.myfont)
        label.grid(column=col, row=row, pady=py, padx=px)
        
    def create_values(self):    
        # Создание переменных для хранения выбранных значений
        self.play_with_var = tk.StringVar()
        self.checker_color_var = tk.StringVar()
        self.board_size_var = tk.StringVar()
        self.animation_speed_var = tk.StringVar()
        self.ai_difficulty_var = tk.StringVar()
        
        # Задание значений по умолчанию
        self.play_with_var.set("Інтелектом")
        self.checker_color_var.set("Білий")
        self.board_size_var.set("Звичайний")
        self.animation_speed_var.set("Середня")
        self.ai_difficulty_var.set("Слаба")
        
        # Создание выпадающих списков
        self.set_label("Грати з:",self.myfont,0,0,5,10)
        self.set_menu(self.play_with_var,self.myfont,1,0,5,10,"Інтелектом","Людиною",0)
        
        self.set_label("Колір шашок:",self.myfont,0,1,5,10)
        self.set_menu(self.checker_color_var,self.myfont,1,1,5,10,"Білий","Чорний",0)
        
        self.set_label("Розмір поля:",self.myfont,0,2,5,10)
        self.set_menu(self.board_size_var,self.myfont,1,2,5,10,"Маленький","Звичайний","Великий")
        
        self.set_label("Швидкість анімації:",self.myfont,0,3,5,10)
        self.set_menu(self.animation_speed_var,self.myfont,1,3,5,10,"Маленька","Середня","Велика")
        
        self.set_label("Важкість ШІ:",self.myfont,0,4,10,5)
        self.set_menu(self.ai_difficulty_var,self.myfont,1,4,10,5,"Слаба","Середня","Висока")
        
        self.ok_button = tk.Button(self.window, text="  OK  ", command=self.ok_button_clicked, font=self.myfont)
        self.ok_button.grid(column=0, row=5, pady=5, columnspan=3)
    
    def get_PLAY_WITH(self):
        return self.PLAY_WITH
    
    def get_PLAYER_SIDE(self):
        return self.PLAYER_SIDE
        
    def get_X_SIZE(self):
        return self.X_SIZE
        
    def get_Y_SIZE(self):
        return self.Y_SIZE
    
    def get_CELL_SIZE(self):
        return self.CELL_SIZE
        
    def get_ANIMATION_SPEED(self):
        return self.ANIMATION_SPEED
    
    def get_MAX_PREDICTION_DEPTH(self):
        return self.MAX_PREDICTION_DEPTH    
