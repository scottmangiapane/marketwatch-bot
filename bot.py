import time
import marketwatch_api

email = input('Email: ')
password = input('Password: ')
game = input('Enter your game: ')
symbol = input('Enter the stock symbol: ')

api = marketwatch_api.MarketWatchAPI()
api.login(email, password)

data = []
initial = api.scan_stock(symbol)
for _ in range(0, 10):
    data.append(initial)

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

while True:
    status = api.scan_status(game)
    direction = 0
    print('Direction:')
    while abs(direction) < 0.02:
        direction = estimate()
        print('  ', direction)
    stock = api.scan_stock(symbol)
    if status['stats']['Buying Power'] >= stock * 1500:
        if direction > 0:
            print('Buy at: ', stock)
            response = api.trade(game, symbol, '1500', 'Buy', None)
            print('Sell at: ', stock + 0.02)
            response = api.trade(game, symbol, '1500', 'Sell', stock + 0.02)
        elif direction < -0:
            print('Short at: ', stock)
            response = api.trade(game, symbol, '1500', 'Short', None)
            print('Cover at: ', stock - 0.02)
            response = api.trade(game, symbol, '1500', 'Cover', stock - 0.02)
