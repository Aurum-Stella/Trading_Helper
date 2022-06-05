from tkinter import *
import tkinter.messagebox
import tkinter.messagebox as mb
import time
import string
from send_email import send_sequrity_code
from random import randint
from sqlDB import DataBase
#from AS_Project_main import Main_screen

class LogIn():
    
    def __init__(self):
        
        self.root = Tk()
        self.root.geometry('500x290')
        self.root.resizable(width=False, height=False)
        self.root.title('LogIn')


        self.ent_email = Entry(self.root,width=20,bd=3)                    #Поле Почты
        self.ent_password = Entry(self.root, show= "*", bd=3)         #Поле пароль
        self.ent_password.place(relx=.5, y=100, anchor="c")
        self.ent_email.place(relx=.5, y=70, anchor="c")


        email_txt = Label(self.root, text="Почта:", font="Arial 9")
        password_txt = Label(self.root, text="Пароль:", font="Arial 9")
        email_txt.place(relx=.30, y=70, anchor="c")
        password_txt.place(relx=.29, y=100, anchor="c")

        
        button_log_in = Button(self.root, text="Войти", width=10,height=1, bg="white",fg="black", command = lambda: self.start_login(self.ent_email.get(), self.ent_password.get()))
        button_log_in.place(relx=.5, y=140, anchor="c", height=25, width=100)

        
        button_registr = Button(self.root, text="Регистрация", width=10,height=1, bg="white",fg="black", command = lambda: self.status_login_window())
        button_registr.place(relx=.5, y=170, anchor="c", height=25, width=100)

        button_remember_password = Button(self.root, text="Восстановить пароль", width=10,height=1, bg="white",fg="black", command = lambda: remember_password(self.root))
        button_remember_password.place(relx=.5, y=210, anchor="c", height=25, width = 140)

        self.c1 = IntVar()
        self.che1 = Checkbutton(self.root,text="Показать пароль",variable=self.c1,onvalue=1,offvalue=0, command = lambda: self.printer(self.c1, [self.ent_password]))
        self.che1.place(relx=.5, y=20, anchor="c")
        

        self.root.mainloop() 


    def start_login(self, email, password):
        data_logIn = DataBase().logIn_verification(email, password)
        if data_logIn:
            self.status_login_window(True)
            #Main_screen(data_logIn[0], data_logIn[1], data_logIn[2])
        
        else:
            Info_block(5)

    def printer(self, value, Entry_):
    
        print(value.get())
        for i in Entry_:
            if value.get():
                i.config(show = "")
            else:
                i.config(show = "*")


    def status_login_window(self, status = False):
        if status:
            self.root.destroy()
        else:
            self.root.destroy()
            Registration_window()
                                                                

class Registration_window(LogIn):
   
    def __init__(self):
        self.RegWindow = Tk()
        self.RegWindow.title('Register')
        self.RegWindow.geometry('500x290')
        self.RegWindow.grab_set()   
        self.RegWindow.focus_set()
        self.RegWindow.resizable(width=False, height=False)
                
        self.ent_name = Entry(self.RegWindow,width=20,bd=3)              #Поле Имя
        self.ent_name.place(relx=.5, y=70, anchor="c")

        self.ent_password = tkinter.Entry(self.RegWindow, show= "*", bd=3)  #Поле пароль
        self.ent_password.place(relx=.5, y=100, anchor="c")

        self.ent_email = Entry(self.RegWindow,width=20,bd=3)               #Поле Email
        self.ent_email.place(relx=.5, y=130, anchor="c")      
        
        self.name_txt = Label(self.RegWindow, text="Ваше имя:", font="Sans 9")
        self.name_txt.place(relx=.26, y=70, anchor="c")

        self.password_txt = Label(self.RegWindow, text="Ваш пароль:", font="Sans 9")
        self.password_txt.place(relx=.25, y=100, anchor="c")

        
        self.email_txt = Label(self.RegWindow, text="Ваша почта:", font="Sans 9")
        self.email_txt.place(relx=.25, y=130, anchor="c")

        button_registration = Button(self.RegWindow, text="Регистрация", width=10,height=1, bg="white",fg="black", command = self.validate_data_reg)
        button_registration.place(relx=.5, y=170, anchor="c", height=25, width=100)

        button_info = Button(self.RegWindow, text="?", bg="white", fg="blue", font="Sans 13", command = lambda: Info_block(1))
        button_info.place(relx=.70, y=100, anchor="c", height=20, width=20)    

        self.c2 = IntVar()
        self.che2 = Checkbutton(self.RegWindow,text="Показать пароль",variable = self.c2, onvalue=1, offvalue=0, command = lambda: self.printer(self.c2, [self.ent_password]))
        self.che2.place(relx=.5, y=20, anchor="c")  

        self.RegWindow.protocol("WM_DELETE_WINDOW", (self.destroy))


    def destroy(self):
        self.RegWindow.destroy()
        LogIn()   


    def validate_data_reg(self):
        valid_name = self.ent_name.get()
        valid_password = self.ent_password.get()
        valid_email = self.ent_email.get()
        self.name_txt.config(fg = 'black')
        self.password_txt.config(fg = 'black')
        self.email_txt.config(fg = 'black')
        if  [i for i in valid_name if i in string.punctuation]\
                                            or not valid_name \
                                            or not valid_name.isalpha()\
                                            or len(valid_name) < 2 or len(valid_name) > 15:                               
            Info_block(1)
            self.name_txt.config(fg = 'red')

        elif  not [i for i in valid_password if i in string.digits ] or \
                                            not [r for r in valid_password if  r in string.ascii_lowercase] or \
                                            not bool(valid_password) or \
                                            len(valid_password) < 5 and len(valid_password) > 20:
            self.name_txt.config(fg = 'black')                                
            Info_block(1)
            self.password_txt.config(fg = 'red')

        elif not '@' in valid_email or not '.' in valid_email:
            self.password_txt.config(fg = 'black')
            Info_block(1)
            self.email_txt.config(fg = 'red')

        else:
            self.email_txt.config(fg = 'black')
            if DataBase().email_availability_check(valid_email):
                self.Verify_email()
            else:
                Info_block(7)



    def Verify_email(self):
        self.email_password = Entry(self.RegWindow,width=20,bd=3) 
        self.email_password.place(relx=.5, y=200, anchor="c")

        self.email_password_txt = Label(self.RegWindow, text="Код с письма:", font="Sans 9")
        self.email_password_txt.place(relx=.26, y=200, anchor="c")

        secur_code = randint(1001, 9999)

        button_verify_email = Button(self.RegWindow, text="Подтвердить", width=10,height=1, bg="white",fg="black", command = lambda: verify_email_code(secur_code))
        button_verify_email.place(relx=.5, y=240, anchor="c")

        Info_block(2, self.ent_email.get())

        send_sequrity_code(1, self.ent_email.get(), secur_code, self.ent_name.get())

        def verify_email_code(code):
            if not int(self.email_password.get()) == code:
                Info_block(3)
            else:
                DataBase().register_new_user(self.ent_name.get(), self.ent_email.get(), self.ent_password.get())
                Info_block(4)

class remember_password(LogIn):
    def __init__(self, master):
        self.remember_password_Window = Toplevel(master)
        self.remember_password_Window.title('Ща восстановим')
        self.remember_password_Window.geometry('500x290')
        self.remember_password_Window.grab_set()   
        self.remember_password_Window.focus_set()
        self.remember_password_Window.resizable(width=False, height=False)
                
        self.send_email = Entry(self.remember_password_Window,width=20,bd=3)              
        self.send_email.place(relx=.5, y=100, anchor="c")

        self.send_email_txt = Label(self.remember_password_Window, text="Введите ниже Ваш адресс эл-почты и нажмите \n 'Восстановить пароль'", font="Sans 9")
        self.send_email_txt.place(relx=.5, y=70, anchor="c")
        
        button_verify_email = Button(self.remember_password_Window, text="Восстановить пароль", width=20,height=1, bg="white",fg="black", command = lambda: recovery_password(self.send_email.get()))
        button_verify_email.place(relx=.5, y=130, anchor="c")


        def recovery_password(email):
            email_DB = self.send_email.get()

            if DataBase().email_availability_check(email):
                print(email)
                Info_block(6, email)
            else:
                secur_code = randint(1001, 9999)
                Info_block(8, self.send_email.get())
                send_sequrity_code(2, self.send_email.get(), secur_code)
                
                send_email_recovery_password = Entry(self.remember_password_Window,width=20,bd=3)              
                send_email_recovery_password.place(relx=.5, y=180, anchor="c")

                button_change_password = Button(self.remember_password_Window, text="Измнить пароль", width=20,height=1, bg="white",fg="black", command = lambda: verify_email_code(secur_code))
                button_change_password.place(relx=.5, y=210, anchor="c")

                def verify_email_code(email_code):
                    print(email_code, self.send_email.get())

                    if int(email_code) == int(send_email_recovery_password.get()):
                        
                        self.send_email.destroy()
                        self.send_email_txt.destroy()
                        button_verify_email.destroy()
                        send_email_recovery_password.destroy()
                        button_change_password.destroy()

                        self.send_email_txt = Label(self.remember_password_Window, text="Введите новый пароль", font="Sans 9")
                        self.send_email_txt.place(relx=.23, y=120, anchor="c")

                        self.ent_password = Entry(self.remember_password_Window,width=20,bd=3, show= "*")              
                        self.ent_password.place(relx=.5, y=120, anchor="c")

                        self.send_email_txt = Label(self.remember_password_Window, text="Повторите пароль",  font="Sans 9")
                        self.send_email_txt.place(relx=.25, y=150, anchor="c")

                        self.re_enter_new_password = Entry(self.remember_password_Window,width=20,bd=3, show= "*")              
                        self.re_enter_new_password.place(relx=.5, y=150, anchor="c")
                        
                        button_confirm_new_password = Button(self.remember_password_Window, text="Подтвердить новый пароль", width=25,height=1, bg="white",fg="black", command = lambda:confirm_password())
                        button_confirm_new_password.place(relx=.5, y=190, anchor="c")

                        self.c3 = IntVar()
                        self.che3 = Checkbutton(self.remember_password_Window,text="Показать пароль",variable = self.c3, onvalue=1, offvalue=0, command = lambda: self.printer(self.c3, [self.ent_password, self.re_enter_new_password]))
                        self.che3.place(relx=.5, y=20, anchor="c")  
                    else:
                        Info_block(3)

                    def confirm_password():
                        if self.ent_password.get() == self.re_enter_new_password.get():
                            if not [i for i in self.ent_password.get() if i in string.digits ] or \
                                            not [r for r in self.ent_password.get() if  r in string.ascii_lowercase] or \
                                            not bool(self.ent_password.get()) or \
                                            len(self.ent_password.get()) < 5 and len(self.ent_password.get()) > 20:
                                Info_block(11)
                            else:
                                DataBase().change_password(email_DB, self.re_enter_new_password.get())
                                Info_block(9)
                                self.remember_password_Window.destroy()
                        else:
                            Info_block(10)
        

    

class Info_block:

    def __init__(self, num, email = None):
        message = {
            1: """Имя должно содержать только символы латинского и кириллического алфавита и быть от 2 до 15 символов.\n  
            Пароль должен состоять из символов латинского алфавита, хотя-бы одной цыфры, быть не менее 5 и не более 20 символов.\n
            Электронная почта требуется для подтверждения о том что вы не робот и восстановления пароля.""",
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
    


if __name__ =='__main__':
    LogIn()
                                                                     