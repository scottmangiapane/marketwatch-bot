import marketwatch_api

email = input('Email: ')
password = input('Password: ')
game = input('Enter your game: ')

api = marketwatch_api.MarketWatchAPI()
api.login(email, password)

while True:
    status = api.scan_status(game)
    stock = api.scan_stock('EXCHANGETRADEDFUND-XASQ-JNUG')
    if status['Buying Power'] > 2 * stock:
        response = api.trade(game, 'EXCHANGETRADEDFUND-XASQ-JNUG', '1', 'Buy', stock + 0.2)
        print(response)
        response = api.trade(game, 'EXCHANGETRADEDFUND-XASQ-JNUG', '1', 'Short', stock - 0.2)
        print(response)
