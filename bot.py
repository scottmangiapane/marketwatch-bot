import time
import marketwatch_api

email = input('Email: ')
password = input('Password: ')
game = input('Enter your game: ')

api = marketwatch_api.MarketWatchAPI()
api.login(email, password)

def estimate():
    net = 0
    prev = api.scan_stock('EXCHANGETRADEDFUND-XASQ-JNUG')
    for i in range(0, 8):
        start = time.time()
        current = api.scan_stock('EXCHANGETRADEDFUND-XASQ-JNUG')
        if current - prev > 0:
            net += 1
        elif current - prev < 0:
            net -= 1
        prev = current
        while time.time() - start < 2:
            pass
    return net

while True:
    status = api.scan_status(game)
    direction = estimate()
    stock = api.scan_stock('EXCHANGETRADEDFUND-XASQ-JNUG')
    if status['stats']['Buying Power'] >= stock * 500:
        if direction > 0:
            response = api.trade(game, 'EXCHANGETRADEDFUND-XASQ-JNUG', '500', 'Buy', stock)
        elif direction < 0:
            response = api.trade(game, 'EXCHANGETRADEDFUND-XASQ-JNUG', '500', 'Short', stock)
