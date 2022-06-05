import smtplib
import traceback
import pymysql.cursors
from config import host, user, password, db_name



    
class DataBase:

    def __init__(self):
       
        self.connection = pymysql.connect(host = host,
                                 port = 3306,
                                 user = user,
                                 password= password,
                                 database= db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        print('Done connection')
    
    def quotes(self, args):
        print(args)
        if isinstance(args, list):
            
            for i in range(len(args)):
                args[i] = "'" + args[i] + "'"
            return(args)        
        else:
            list_ = list(args)
        for i in range(len(list_)):
            list_[i] = "'" + list_[i] + "'"
            return list_
            

    def request_sql(self, request_, commit = False):
        print(request_)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(request_)
                if commit:
                    self.connection.commit()    
                
                rows = cursor.fetchall()
                return(rows)
        finally:
            self.connection.close()
             

    def change_password(self, email, new_password):
        users_data = self.quotes(email, new_password)

        check_id_sql = f"select id_users from users_data where email_users = {users_data[0]}"

        check_id = self.request_sql(check_id_sql)
        
        id = check_id[0]['id_users']
        change_password = f"UPDATE users_data SET password_users = {users_data[1]} WHERE id_users = {id}"
        
        DataBase().request_sql(change_password, True)
       

    def email_availability_check(self, email):
        users_data = self.quotes(email)
        check_login = f"SELECT email_users FROM users_data WHERE email_users = {users_data[0]}"
        rows = self.request_sql(check_login)
        if rows:
            return False
        else:
            
            return True 


    def logIn_verification(self, email_users, password_users):
        users_data = self.quotes(email_users, password_users)
        check_login = f"SELECT email_users FROM users_data WHERE email_users = {users_data[0]} and password_users = {users_data[1]};"
        rows = self.request_sql(check_login)
        

        if not rows:
            
            return False
             
        else:
            sql_request = f'SELECT id_users, name_users, email_users FROM users_data WHERE email_users = {users_data[0]}'
            rows = DataBase().request_sql(sql_request)
            print(rows)      
            print('Вы авторизировались')
            data = [rows[0][i] for i in rows[0]] 
            return data
        

    def register_new_user(self, name, email, password):
        users_data = self.quotes(name, email, password)
        insert = [f"INSERT INTO users_data SET name_users = {users_data[0]}, email_users = {users_data[1]}, password_users = {users_data[2]}", \
            "INSERT INTO bottom_info SET first_bottom = 'BTCUSDT', second_bottom = 'ETHUSDT', third_bottom = 'XRPUSDT', fourth_bottom = 'BNBUSDT', fifth_bottom = 'USDTUAH'"]

        for i in insert:
            DataBase().request_sql(i, True)
        
        print('Регистрация прошла успешно')

    def change_coin_with_bottom(self, id_users, list_coin):
        list_coins = self.quotes(list_coin)
        insert = f"UPDATE bottom_info SET first_bottom = {list_coins[0]}, second_bottom = {list_coins[1]}, third_bottom = {list_coins[2]}, fourth_bottom = {list_coins[3]}, fifth_bottom = {list_coins[4]} WHERE id_users = {id_users}"
        print(id_users, list_coins)
        self.request_sql(insert, True)


    def get_coin_in_botton(self, id_users):
        insert = f"SELECT * FROM bottom_info WHERE id_users={id_users}"
        rows = self.request_sql(insert)[0]
        print(rows, 'qwe')
        result = [rows[val] for val in rows][0:]
        return result[1:]

       # print(result)


requests_ = {
    "register_new_user": 
        ["INSERT INTO users_data SET name_users = {users_data[0]}, email_users = {users_data[1]}, password_users = {users_data[2]}",\
        "INSERT INTO bottom_info SET first_bottom = 'BTCUSDT', second_bottom = 'ETHUSDT', third_bottom = 'XRPUSDT', fourth_bottom = 'BNBUSDT', fifth_bottom = 'USDTUAH'"],
    "logIn_verification": [],
}


            


#DataBase().change_coin_with_bottom(1, ['BTCUSDT', 'BTCUSDT', 'BTCUSDT', 'BTCUSDT', 'BTCUSDT'])