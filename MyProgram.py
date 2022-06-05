from tkinter import *
import tkinter.messagebox
import tkinter.messagebox as mb
import time
import string
from send_email import send_sequrity_code
from random import randint
from sqlDB import DataBase


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

        
        button_log_in = Button(self.root, text="Войти", width=10,height=1, bg="white",fg="black", command = lambda : DataBase().logIn_verification(self.ent_email.get(), self.ent_password.get()) )
        #button_log_in.bind("<Button-1>", (lambda x: DataBase().logIn_verification(self.ent_email.get(), self.ent_password.get())))


        
        button_log_in.place(relx=.5, y=140, anchor="c", height=25, width=100)
        button_registr = Button(self.root, text="Регистрация", width=10,height=1, bg="white",fg="black", command = self.open_registration_window)
        button_registr.place(relx=.5, y=170, anchor="c", height=25, width=100)


        self.c1 = IntVar()
        self.che1 = Checkbutton(self.root,text="Показать пароль",variable=self.c1,onvalue=1,offvalue=0)
        self.che1.bind("<Button-1>", (lambda  c1 = self.c1: self.printer(self.c1)))
        self.che1.place(relx=.5, y=20, anchor="c")


        self.root.mainloop() 

 
    def printer(self, value):
        print(value.get())       
        if not value.get():
            self.ent_password.config(show = "")
        else:
            self.ent_password.config(show = "*")


    def open_registration_window(self):
        self.close_main_window(False)
        Registration_window(self.root)


    def close_main_window(self, bool_):
        if bool_:
            self.root.deiconify()
        else:
            self.root.withdraw()                                            #Скрыть главное окно 
                                                                            #self.root.deiconify() отобразить     
        


class Registration_window(LogIn):
   
    def __init__(self, master):
        self.RegWindow = Toplevel(master)
        self.RegWindow.title('Register')
        self.RegWindow.geometry('500x290')
        self.RegWindow.grab_set()   
        self.RegWindow.focus_set()
        self.RegWindow.resizable(width=False, height=False)
        
        
        self.ent_name = Entry(self.RegWindow,width=20,bd=3)              #Поле Имя
        self.ent_password = tkinter.Entry(self.RegWindow, show= "*", bd=3)  #Поле пароль
        self.ent_email = Entry(self.RegWindow,width=20,bd=3)               #Поле Email
        self.ent_name.place(relx=.5, y=70, anchor="c")
        self.ent_password.place(relx=.5, y=100, anchor="c")
        self.ent_email.place(relx=.5, y=130, anchor="c")
        
        
        self.name_txt = Label(self.RegWindow, text="Ваше имя:", font="Sans 9")
        self.password_txt = Label(self.RegWindow, text="Ваш пароль:", font="Sans 9")
        self.email_txt = Label(self.RegWindow, text="Ваша почта:", font="Sans 9")


        self.name_txt.place(relx=.26, y=70, anchor="c")
        self.password_txt.place(relx=.25, y=100, anchor="c")
        self.email_txt.place(relx=.25, y=130, anchor="c")


        button_registration = Button(self.RegWindow, text="Регистрация", width=10,height=1, bg="white",fg="black", command = self.validate_data_reg)
        button_registration.place(relx=.5, y=170, anchor="c", height=25, width=100)


        button_info = Button(self.RegWindow, text="?", bg="white", fg="blue", font="Sans 13")
        button_info.bind("<Button-1>", (lambda info: valid_data_info()))
        button_info.place(relx=.70, y=100, anchor="c", height=20, width=20)    


        self.c2 = IntVar()
        self.che2 = Checkbutton(self.RegWindow,text="Показать пароль",variable = self.c2, onvalue=1, offvalue=0)
        self.che2.bind("<Button-1>", (lambda  c2 = self.c2: self.printer(self.c2)))
        self.che2.place(relx=.5, y=20, anchor="c")  


        self.RegWindow.protocol("WM_DELETE_WINDOW",  (self.destroy))

    def destroy(self):
        self.RegWindow.destroy()
        LogIn().close_main_window(True)   



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
                                           
            valid_data_info()
            self.name_txt.config(fg = 'red')

        elif  not [i for i in valid_password if i in string.digits ] or \
                                            not [r for r in valid_password if  r in string.ascii_lowercase] or \
                                            not bool(valid_password) or \
                                            len(valid_password) < 5 and len(valid_password) > 20:
            self.name_txt.config(fg = 'black')                                
            valid_data_info()
            self.password_txt.config(fg = 'red')

        elif not '@' in valid_email or not '.' in valid_email:
            self.password_txt.config(fg = 'black')
            valid_data_info()
            self.email_txt.config(fg = 'red')

        else:
            self.email_txt.config(fg = 'black')
            self.Verify_email()

    def Verify_email(self):
        self.email_password = Entry(self.RegWindow,width=20,bd=3) 
        self.email_password.place(relx=.5, y=200, anchor="c")

        self.email_password_txt = Label(self.RegWindow, text="Код с письма:", font="Sans 9")
        self.email_password_txt.place(relx=.26, y=200, anchor="c")


        secur_code = randint(1001, 9999)

        button_verify_email = Button(self.RegWindow, text="Подтвердить", width=10,height=1, bg="white",fg="black")
        button_verify_email.bind("<Button-1>", (lambda  code: verify_email_code(secur_code)))
        button_verify_email.place(relx=.5, y=240, anchor="c")
        info_email_message(self.ent_email.get())

        send_sequrity_code(secur_code, self.ent_email.get(), self.ent_name.get())

        def verify_email_code(code):
            
            if not int(self.email_password.get()) == code:
                Incorrect_email_code()
            else:
                DataBase().register_new_user(self.ent_name.get(), self.ent_email.get(), self.ent_password.get())
                Registration_complite()


class valid_data_info(Registration_window):
    
    def __init__(self):
        
        msg = """ 
            Имя должно содержать только символы латинского и кириллического алфавита и быть от 2 до 15 символов.\n  
            Пароль должен состоять из символов латинского алфавита, хотя-бы одной цыфры, быть не менее 5 и не более 20 символов.\n
            Электронная почта требуется для подтверждения о том что вы не робот и восстановления пароля.           
            """
         
        mb.showinfo("Информация", msg)       
        print(mb)
    
    
class info_email_message(Registration_window):
    
    def __init__(self, email):
        
        msg = f""" 
            На почту {email} был отправлен код подтверждения. Если Вы не получили код, проверьте корректность ввода эл-почты, или попробуйте другой адресс. 
            """
         
        mb.showinfo("Информация", msg)       
        print(mb)  

class Incorrect_email_code(Registration_window):
    
    def __init__(self):
        
        msg = f""" 
            Не верный код подтверждения. Перепроверьте правильность ввода, или попробуйте отправить еще раз. 
            """
         
        mb.showinfo("Информация", msg)       
        print(mb)  
        

class Registration_complite(Registration_window):
    
    def __init__(self):
        
        msg = f""" 
            Регистрация прошла успешно, для того что бы продолжить, закройте окно регистрации и авторизуйтесь. 
            """
         
        mb.showinfo("Информация", msg)       
        print(mb)  


class Incorrect_data(Registration_window):
    
    def __init__(self):
        
        msg = f""" 
            Не верный логин или пароль, проверьте корректность вводных данных. Или пройдите регистрацию. 
            """
         
        mb.showinfo("Информация", msg)       
        print(mb)  


if __name__ =='__main__':
    LogIn()

     