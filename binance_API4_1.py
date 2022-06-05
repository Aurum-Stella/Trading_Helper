import json
import requests
import time
import statistics
import pandas as pd
import numpy as np




class Static_data:
    """https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md"""
    """https://coinmarketcap.com/ru/exchanges/binance/"""

        # Binance API
        # Текущаю цена
    current_average_price_link = 'https://api3.binance.com/api/v3/avgPrice'
        # Свечные данные ([1]Open, [2]Hight, [3]Low, [4]Close)
    candlestick_data_link = 'https://api1.binance.com/api/v3/klines'

        # Coinmarketcap GET JSON
        # Список торговых пар
    count = 1000
    get = f'https://api.coinmarketcap.com/data-api/v3/exchange/market-pairs/latest?slug=binance&category=spot&start=1&limit={count}'
    headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
}

    two_h = '%.0f'%((time.time()-1440000)*1000)
    eight_h = '%.0f'%((time.time()-5760000)*1000)
    one_day = '%.0f'%((time.time()-17280000)*1000)
    global_interval = {'2h': two_h, '8h' : eight_h, '1d': one_day}


class Coins_data(Static_data):
    coins = []
    

    def get_coins_coinmarketcap(self):
        
        req = requests.get(self.get, headers = self.headers)
        src = req.json()
        for i in range(len(src['data']['marketPairs'])):
            self.coins.append(src['data']['marketPairs'][i]['marketPair'])
        self.init_and_write_coins_in_json()
                   
        return(self.coins)
        
        
    
    def init_and_write_coins_in_json(self): #staticmethod??
        coins_json = {}
        for i in self.coins:
            slice_right = i[i.find('/')+1:]
            if coins_json.get(slice_right, False) == False: 
                coins_json[slice_right] = []
                for n in self.coins:             
                    if slice_right == n[n.find('/')+1:]:
                        coins_json[slice_right].append(n[:n.find('/')])
            with open('DB.json', 'w') as w:
                json.dump(coins_json, w, indent=4)
                #return(self.formating_for_list_ParaPara(coins_list, coins_json))


    """def formating_for_list_ParaPara(self):            
        сoins = [i.replace("/", "") for i in self.coins]
        
        return(сoins)"""


class Candlestick(Static_data):

    def __init__(self, coin = 'BTCUSDT', interval = '1d', start_time = '1'):
        self.coin = coin
        self.interval = interval
        self.start_time = start_time

    def get_average_price(self, coin):
        response = requests.get(self.current_average_price_link, {'symbol': f'{coin}'})
        global_price =  response.json()
        print(global_price["price"])
        return(global_price["price"])

    def get_and_write_candlestick_data_binance(self, coin, interval, start_time): 
        response = requests.get(self.candlestick_data_link, {'symbol': coin, 'interval': interval, 'startTime': start_time})
        global_price = [list(map(float, i)) for i in response.json()]
        global_price.reverse()
        return(global_price)
    """def get_and_write_candlestick_data_binance(self, coin, interval, start_time): 
        response = requests.get(self.candlestick_data_link, {'symbol': coin, 'interval': interval, 'startTime': start_time})
        global_price = [float(item) for l in response.json() for item in l]
        
        global_price.reverse()  
        return(global_price)"""


# Калькулятор изменения цены по периодам (1,7,14,31). 
# Находит в каждом периоде макс и мин значение и выводит среднее арифметическое.
# Если среднее больше текущей цены - цена просела больше чем выросла,
# вычесляем процентную разнуцу между макс и текущим значением 
# и наоборот
class Calculator_prozent:

    def calculator_prozent(self, price): #Staticmethod???

        def raznica(a, b):
            if a > b:
                return(-((a-b)/a) * 100)
            else:
                return(((b-a)/a) * 100)


        open_price, close_price = [i[1] for i in price], [i[4] for i in price]
        now_period = raznica(open_price[0], close_price[0])

        if len(price) > 7:
            if statistics.mean([max(close_price[1:8]), min(close_price[1:8])]) < close_price[0]:
                seven_period = raznica(min(close_price[1:8]), close_price[0])
            else:
                seven_period = raznica(max(close_price[1:8]), close_price[0])
        else:
            return('%.1f'%(now_period))        
        if len(price) > 14:
            if statistics.mean([max(close_price[1:15]), min(close_price[1:15])]) < close_price[0]:
                forteen_period = raznica(min(close_price[1:15]), close_price[0])
            else:
                forteen_period = raznica(max(close_price[1:15]), close_price[0])
        else:
            return('%.1f'%(now_period), '%.1f'%(seven_period),)        
        if len(price) > 31:
            if statistics.mean([max(close_price[1:32]), min(close_price[1:32])]) < close_price[0]:
                month_period = raznica(min(close_price[1:32]), close_price[0])
            else:
                month_period = raznica(max(close_price[1:32]), close_price[0])
        else:
            return('%.1f'%(now_period), '%.1f'%(seven_period), '%.1f'%(forteen_period))        
        return('%.1f'%(now_period), '%.1f'%(seven_period), '%.1f'%(forteen_period),'%.1f'%(month_period))

# Индикатор: Полосы болинджера.
# Индикатор представляет из себя три скользящие линии которые образуют некий "тунель". 
# Цена 80% времени находится в данном тунеле
# "Пробитие" цены одной из линий говорит о сильной вероятности разворота цены.
# В данном случае индикатор выводит 3 числа - Верхняя, центральная, нижняя линия соответственно.
# Отрицательное значение говорит о том что цене "опускаться" до нужной линии еще столько-то процентов.
# Положительное значение говорит о том что цене "расти" до нужно линии еще столько-то процентов.
class Bollinger_bands:
    
    def calculator_BB(self, now_price, oll_price):     #staticmethod??
        price = []

        if len(oll_price) > 13:
            price = [oll_price[i][4] for i in range(13)]
        elif len(oll_price) < 5:
            return('Недостаточно данных')    
        else: 
            price = [oll_price[i][4] for i in range(len(oll_price))]

        ML = statistics.mean(price)
        TL = ML+(2*statistics.stdev(price))  
        BL = ML-(2*statistics.stdev(price))
                     #Узнали, записали среднее значеие выборки (MidLine)   
        BB = [TL,ML,BL]

        for i in range(len(BB)):
            BB[i] = (BB[i]-now_price)/now_price*100    
        return(BB)


class RSI:
    # Индикатор RSI: индекс относительной силы.
# На выход подает значение от 0 до 100, чем значение выше/ниже, тем больше шанс разворота цены.
# Обычно отслеживают значение 30 и ниже/ 70 и выше. 
# В данном случае программа отслеживает значение 30 и ниже.
    def rsi_tradingview(self, period: int = 14, round_rsi: bool = True, global_price=[]): #staticmethod???
        ohlc = []

        if len(global_price) > 200:
            for i in range(200):
               ohlc.append(float(global_price[i][4]))
        else: 
            for i in range(len(global_price)):
                ohlc.append(float(global_price[i][4])) 
        ohlc.reverse()            
        ohlc = pd.Series(ohlc)

        delta = ohlc.diff()

        up = delta.copy()
        up[up < 0] = 0
        up = pd.Series.ewm(up, alpha=1/period).mean()

        down = delta.copy()
        down[down > 0] = 0
        down *= -1
        down = pd.Series.ewm(down, alpha=1/period).mean()

        rsi = np.where(up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down))))

        return(np.round(rsi, 2).tolist())



# Поиск дивергенций:
# Разхождение в графике RSI и ценовом говорит о смене тренда.
# Если расхождения замечены по вершинам графиков - болоьшая вероятность падения цены.
# Данный код ищет девергенции на рост.
# График нужно проверять, реализация сыровата.
class Divergere:
    def divergere(self, rsi, price):  #staticmethod???
        price.reverse()
        price_clouse_down = [price[i+1][4] for i in range(len(price)-2) if price[i+1][4] < price[i][4] and price[i+1][4] < price[i+2][4]]
        rsi_down = [rsi[i+1] for i in range(len(rsi)-2) if rsi[i+1] < rsi[i] and rsi[i+1] < rsi[i+2]]
        
        price_clouse_down.reverse() 
        rsi_down.reverse()
        min_len = min([len(price_clouse_down), len(rsi_down)])
        if min_len > 10:
            min_len = 11
        for i in range(1, min_len):
            if (price_clouse_down[0] < price_clouse_down[i] and rsi_down[0] < rsi_down[i])  or  (price_clouse_down[0] > price_clouse_down[i] and rsi_down[0] > rsi_down[i]):
                continue
            else:
                return(price_clouse_down[i], i, rsi_down[i])
        return(0, 0, 0)


# Линии поддержки и сопротевления при достижении которых цена с большей вероятностью пойдет в прот. сторону.

class Pivot_point(Candlestick):

    

    def __init__(self, coin, interval):
        self.coin = coin
        self.interval = interval
        
    

    def pricePP(self):

        period = {  '2h': ['%.0f'%((time.time()-169200)*1000), '1d'], #1d
                    '8h': ['%.0f'%((time.time()-342000)*1000), '1d'], #3d
                    '1d': ['%.0f'%((time.time()-561605)*1000), '1d']  #6d
        }

        price_data = super().get_and_write_candlestick_data_binance(self.coin, period[self.interval][1], period[self.interval][0])

        if len(price_data) < 2:
            return('Невозможно рассчитать линии поддержки и сопротивления')


        def raznica(a, b):
            if a > b:
                return['%.3f'%(a), '%.1f'%(((a-b)/a) * 100)]
            else:
                return['%.3f'%(a), '%.1f'%(-((b-a)/a) * 100)]


        open_price = price_data[-1][1]
        hight_price = max([i[2] for i in price_data[1:]])
        low_price = min([i[3] for i in price_data[1:]])
        close_price = price_data[1][4]
        now_price = price_data[0][4]

        pivotPoint = (hight_price+low_price+close_price)/3 
        
        
        R3 = raznica((hight_price+2*(pivotPoint - low_price)), now_price)
        R2 = raznica((pivotPoint + (hight_price - low_price)), now_price)
        R1 = raznica((2*pivotPoint - low_price), now_price)
        S1 = raznica((2*pivotPoint - hight_price), now_price)
        S2 = raznica((pivotPoint - (hight_price - low_price)), now_price)
        S3 = raznica((low_price - 2*(hight_price - pivotPoint)), now_price)

        return(R1,R2,R3,S1,S2,S3)
        
        

# Перебор торговых пар и периодов в формате ['BTCUSDT']
class Сounting(Coins_data, Candlestick):
    
    def __init__(self, coins_list = None):
#        if not requests.get("http://www.binance.com").status_code == 200:
#            return "no internet connection"
        self.coins_list = coins_list
        if self.coins_list == None:
            coins = super().get_coins_coinmarketcap()
            print(coins)
            self.coins_list = [i.replace("/", "") for i in coins]
            self.counting_coins_and_interval(self.coins_list)
        else:
            if __name__ =='__main__':
                self.counting_coins_and_interval(coins_list) 
                
        
    def counting_coins_and_interval(self, coins):    
        for c in coins:        
            for i in self.global_interval:
                self.candlestick_data = super().get_and_write_candlestick_data_binance(c, i, self.global_interval[i])
                print(c,i)
                print(Calculator_prozent().calculator_prozent(self.candlestick_data))
                print(Bollinger_bands().calculator_BB(self.candlestick_data[0][4], self.candlestick_data))
                rsi = RSI().rsi_tradingview(global_price = self.candlestick_data)
                print(rsi[-1])
                print(Divergere().divergere(rsi, self.candlestick_data))
                #print(Pivot_point(c, i).pricePP())

    def counting_coins_and_interval_desctop(self):
        coin_price = float(super().get_average_price(self.coins_list))
        print(coin_price, 'тот самый')

        
        return(coin_price)
       

# формат ввода <BTCUSDT,ETHUSDT,XRPBTC> и тд. без пробелов.
if __name__ =='__main__':
    coins = input()
    if coins == "":
        Сounting()
    else:
        print(coins.split(","))
        Сounting(coins.split(","))

