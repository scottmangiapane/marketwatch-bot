import marketwatch_api

email = input('Email: ')
password = input('Password: ')
game = input('Enter your game: ')

api = marketwatch_api.MarketWatchAPI()
api.login(email, password)

while True:
    status = api.scan_status(game)
    stock = api.scan_stock('EXCHANGETRADEDFUND-XASQ-JNUG')
    if status['stats']['Buying Power'] > 20 * stock:
        response = api.trade(game, 'EXCHANGETRADEDFUND-XASQ-JNUG', '10', 'Buy', stock + 0.2)
        print('Bought at ', stock + 0.02)
        response = api.trade(game, 'EXCHANGETRADEDFUND-XASQ-JNUG', '10', 'Short', stock - 0.2)
        print('Shorted at ', stock - 0.02)
