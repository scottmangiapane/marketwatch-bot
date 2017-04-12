import time
import marketwatch_api

def reset_data():
    initial = api.scan_stock(symbol)
    for _ in range(0, 30):
        data.append(initial)
        data.pop(0)

def estimate():
    start = time.time()
    data.append(api.scan_stock(symbol))
    data.pop(0)
    diff = 0
    for i in range(1, len(data)):
        diff += data[i] - data[i - 1]
    while time.time() - start < 2:
        pass
    return diff

email = input('Email: ')
password = input('Password: ')
game = input('Enter your game: ')
symbol = input('Enter the stock symbol: ')

api = marketwatch_api.MarketWatchAPI()
api.login(email, password)

data = []
reset_data()

while True:
    status = api.scan_status(game)
    direction = 0
    print('Direction:', end='', flush=True)
    while abs(direction) < 0.015:
        direction = estimate()
    stock = api.scan_stock(symbol)
    if status['stats']['Buying Power'] < stock * 2000:
        print('ERROR: Not enough funds')
    else:
        print(round(direction, 4))
        reset_data()
        if direction > 0:
            print('Buy at:', stock)
            response = api.trade_normal(game, symbol, '2000', 'Buy', 'Cancelled')
            print('Sell at:', stock + 0.02)
            response = api.trade_limit(game, symbol, '2000', 'Sell', 'Cancelled', stock + 0.02)
        elif direction < -0:
            print('Short at:', stock)
            response = api.trade_normal(game, symbol, '2000', 'Short', 'Cancelled')
            print('Cover at:', stock - 0.02)
            response = api.trade_limit(game, symbol, '2000', 'Cover', 'Cancelled', stock - 0.02)
