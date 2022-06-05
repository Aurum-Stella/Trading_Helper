from tkinter import *
import tkinter.messagebox
import tkinter.messagebox as mb
from tkinter import ttk
from time import sleep
import json
import datetime
import string
import threading 
from send_email import send_sequrity_code
from random import randint
from sqlDB import DataBase
from binance_API4_1 import Сounting



class Main_screen:
   
    def __init__(self, id_user, name, email):
        print(id_user, name, email)
        self.id = id_user
        self.name = name
        self.email = email
        
        self.main_screen = Tk()
        
        self.main_screen.geometry('1200x600')
        self.main_screen.resizable(width=False, height=False)
        self.main_screen.title('Aurum_Stella')

        self.bottom = Frame(self.main_screen, width=1200, height=20, bg="grey",bd=20)
        self.bottom.place(relx=.5, y=590, anchor="c")
        
        self.id_user_txt = Label(self.main_screen, text=f"id: {self.id}; User: {self.name}", font="Arial 10", bg="grey", fg="white")
        self.id_user_txt.place(x= 50 ,y=591, anchor="c")
        
        self.data_time_txt = Label(self.main_screen, text=f'as', font="Arial 10", bg="grey", fg="white")
        self.data_time_txt.place(x= 1120 ,y=591, anchor="c")

        self.button = ["self.button_info_1", "self.button_info_2", "self.button_info_3", "self.button_info_4", "self.button_info_5"]
        x = 250
        for i in range(5):
            self.button[i] = Button(self.main_screen, text=f"NuN", bg="grey", fg="white", font="Sans 10", command = lambda: change_coin_window(self.id))
            self.button[i].place(x = x, y=591, anchor="c", height=20, width=170)
            x += 170


        
        t1 = threading.Thread(target = lambda: self.data_time_exchange_bottom(self.id))      
        t1.start()
        
        self.main_screen.mainloop()
        
    
        

    def data_time_exchange_bottom(self, id_user):
        
        while True:
            list_coin_buttom = DataBase().get_coin_in_botton(id_user)
            for i in range(5):
                
                sleep(1)
                print(list_coin_buttom, 'list_coin')

                now = datetime.datetime.now()
                self.data_time_txt.config(text = f'{now.strftime("%d-%m-%Y %H:%M")}')
            
                now_price = Сounting(coins_list = list_coin_buttom[i]).counting_coins_and_interval_desctop()
                print(now_price, 'now_price')
            
                self.button[i].config(text = f'{list_coin_buttom[i]}: ' + '%.3f'%(now_price))
      

class change_coin_window(Main_screen):

    def __init__(self, id_user):
        self.id_user = id_user
        self.change_coin_window = Toplevel()
        self.change_coin_window.geometry('1200x600')
        self.book = ttk.Notebook(self.change_coin_window)
        

        self.first_bottom = Label(self.change_coin_window, bg="#f5f5f5", bd=4, relief=RAISED, text="NoN")
        self.first_bottom.place(relx=0.85, rely=0.10, relheight=0.06, relwidth=0.1, anchor="c")

        self.second_bottom = Label(self.change_coin_window, bg="#f5f5f5", bd=4, relief=RAISED, text="NoN")
        self.second_bottom.place(relx=0.85, rely=0.20, relheight=0.06, relwidth=0.1, anchor="c")

        self.third_bottom = Label(self.change_coin_window, bg="#f5f5f5", bd=4, relief=RAISED, text="NoN")
        self.third_bottom.place(relx=0.85, rely=0.30, relheight=0.06, relwidth=0.1, anchor="c")

        self.fourth_bottom = Label(self.change_coin_window, bg="#f5f5f5", bd=4, relief=RAISED, text="NoN")
        self.fourth_bottom.place(relx=0.85, rely=0.40, relheight=0.06, relwidth=0.1, anchor="c")

        self.fifth_bottom = Label(self.change_coin_window, bg="#f5f5f5", bd=4, relief=RAISED, text = "NoN")
        self.fifth_bottom.place(relx=0.85, rely=0.50, relheight=0.06, relwidth=0.1, anchor="c")

        self.info_txt = Label(self.change_coin_window, bg="#f5f5f5", font="Sans 10", text = """
Выделите нужный чек-бокс справа, 
после чего выберите нужную 
торговую пару слева.
После подтверждения,
список монет в нижней части программы
измениться автоматически
в течении 5 секунд. 
    """)
        self.info_txt.place(relx=0.86, rely=0.7, anchor="c")


        self.var = IntVar()
        self.rad1 = Radiobutton(self.change_coin_window,text="1", variable=self.var,value=1)
        self.rad1.place(relx=0.95, rely=0.1,  anchor="c")
        self.rad2 = Radiobutton(self.change_coin_window,text="2", variable=self.var,value=2)
        self.rad2.place(relx=0.95, rely=0.2,  anchor="c")
        self.rad3 = Radiobutton(self.change_coin_window,text="3", variable=self.var,value=3)
        self.rad3.place(relx=0.95, rely=0.3,  anchor="c")
        self.rad4 = Radiobutton(self.change_coin_window,text="4", variable=self.var,value=4)
        self.rad4.place(relx=0.95, rely=0.4,  anchor="c") 
        self.rad5 = Radiobutton(self.change_coin_window,text="5", variable=self.var,value=5)
        self.rad5.place(relx=0.95, rely=0.5,  anchor="c")

        self.button_confirm = Button(self.change_coin_window, text="Подтвердить", width=10,height=1, bg="white",fg="black", font="Sans 13", command = lambda id_users = self.id_user:self.confirm_change_coin_bottom(id_users))
        self.button_confirm.place(relx=.85, rely=0.87, anchor="c", height=30, width = 140)

        self.get_coin_sql()
        self.open_window()
        

    def get_coin_sql(self):
        coin_list_botton = DataBase().get_coin_in_botton(self.id_user)
        self.first_bottom.config(text = f'{coin_list_botton[0]}')
        self.second_bottom.config(text = f'{coin_list_botton[1]}')
        self.third_bottom.config(text = f'{coin_list_botton[2]}')
        self.fourth_bottom.config(text = f'{coin_list_botton[3]}')
        self.fifth_bottom.config(text = f'{coin_list_botton[4]}')
        print(coin_list_botton)
        

    def change_coin_with_button(self, tabs, coin):
        buttons = {1:self.first_bottom, 2:self.second_bottom, 3:self.third_bottom, 4:self.fourth_bottom, 5:self.fifth_bottom}
        radio_button = self.var.get()
        if not radio_button:
            print("aaa")
        else: 
            buttons[radio_button].config(text = f"{coin+tabs}")
            
    def confirm_change_coin_bottom(self, id_user):
        buttons = {1:self.first_bottom, 2:self.second_bottom, 3:self.third_bottom, 4:self.fourth_bottom, 5:self.fifth_bottom}
        values = []
        for i in buttons.keys():
            print(buttons[i].cget("text"))
            values.append(buttons[i].cget("text"))
        print(values) 
        DataBase().change_coin_with_bottom(id_user, values)
        self.change_coin_window.destroy()
          

    def open_window(self):
        
        def configure(event):
            canvas = event.widget
            canvas.configure(scrollregion=canvas.bbox("all"))
        with open('DB.json', 'r') as w:
        
            oll_dict = json.load(w)
            oll_keys = [i for i in oll_dict.keys()]
            print(oll_keys)

        for i in oll_keys:
            column = 0
            row = 0
            tab2 = Frame(self.book, width=300, height=120)
            #tab2.pack_propagate(0)
            self.book.add(tab2, text=f'/{i}')
            self.book.pack(expand=1, fill=BOTH)
            canvas1 = Canvas(tab2)
            vscroll1 = Scrollbar(tab2, orient=VERTICAL, command=canvas1.yview)
            vscroll1.pack(side=RIGHT, fill=Y, expand=0)
            canvas1.configure(yscrollcommand=vscroll1.set)
            canvas1.pack(side=LEFT, fill=BOTH, expand=1)
            frame1 = Frame(canvas1)
            canvas1.create_window((0, 0), window=frame1, anchor=CENTER)

            for r in oll_dict[i]:
                if column > 6:
                    column = 0
                    row += 1
                Button(frame1, text=f"{r}",  width = 15, height = 2, command = lambda tabs = i, coin=r: self.change_coin_with_button(tabs, coin)).grid(row=row, column=column, padx=5, pady=5)
                column += 1
            canvas1.bind('<Configure>', configure)
    
    


class Info_block:
    def __init__(self, num, email = None):
            message = {
                1: """Отсутствует подключение к интернету. Установите соединение и попробуйте еще раз""",
                2: f"""На почту {email} был отправлен код подтверждения. Если Вы не получили код, проверьте корректность ввода эл-почты, или попробуйте другой адресс.""",
                3: """Не верный код подтверждения. Перепроверьте правильность ввода, или попробуйте отправить еще раз.""",
                4: """Регистрация прошла успешно, для того что бы продолжить, закройте окно регистрации и авторизуйтесь.""",
                5: """Не верный логин или пароль, проверьте корректность вводных данных. Или пройдите регистрацию.""",
                6: f"""Электронная почта по адресу {email} не найдена, проверьте корректность адреса, или используйте другой адрес эл-почты.""",
                7: """Данный адресс эл-почты уже зарегистрирован в нашей базе, попробуйте воспользоваться другой почтой. Если вы не можете вспомнить пароль, воспользуйтесь функцией 'Восстановить пароль'""",
                8: f""""На адресс {email} был выслан код восстаовления. Введите его в поле ниже, после этого Вам будет предложено придумать новый пароль""",
                9: """Пароль успешно изменен!!!""",
                10: """Пароли не совпадают, перепроверьте вводные данные""",
                11: """Пароль должен состоять из символов латинского алфавита, хотя-бы одной цыфры, быть не менее 5 и не более 20 символов."""
            }
            mb.showinfo("Информация", message[num])       
            print(mb) 
            
            
           
 

Main_screen(1, "vlad", "vladmeloman7@gmail.com")    


