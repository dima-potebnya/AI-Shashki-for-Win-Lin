from tkinter import Tk, PhotoImage
from checkers.buttons import Buttons

def main():   
    # Створення вікна
    main_window = Tk()
    main_window.title('Шашки')
    main_window.resizable(0, 0)
    main_window.iconphoto(False, PhotoImage(file='icon.png'))
    buttons = Buttons(main_window)
    main_window.mainloop()
    
if __name__ == '__main__':
    main()
