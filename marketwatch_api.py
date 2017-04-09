import json
import status_parser
import stock_parser
import requests

class MarketWatchAPI:
    def __init__(self):
        self.status_parser = status_parser.StatusParser()
        self.stock_parser = stock_parser.StockParser()
        self.session = requests.Session()

    def login(self, email, password):
        id_url = 'http://id.marketwatch.com/auth/submitlogin.json'
        id_headers = {
            'Content-Type': 'application/json',
        }
        id_json = {
            'username': email,
            'password': password,
            'savelogin': 'true',
        }
        id_response = self.session.post(url=id_url, headers=id_headers, json=id_json)
        try:
            self.session.get(url=json.loads(id_response.text)['url'])
        except KeyError:
            print('Login failed.')
            exit(1)

    def scan_status(self, game):
        status_response = self.session.get('http://www.marketwatch.com/game/' + game + '/portfolio/Orders')
        self.status_parser.feed(status_response.text)
        return self.status_parser.get_data()

    def scan_stock(self, fuid):
        stock_response = self.session.get('http://www.marketwatch.com/game/d/trade/getpopup?fuid=' + fuid)
        self.stock_parser.feed(stock_response.text)
        return self.stock_parser.get_data()

    def trade(self, game, name, shares, mode, limit):
        game_url = 'http://www.marketwatch.com/game/' + game + '/trade/submitorder'
        game_headers = {
            'Content-Type': 'application/json',
        }
        game_json = [{'Fuid': name, 'Shares': shares, 'Type': mode, 'Limit': limit}]
        game_response = self.session.post(url=game_url, headers=game_headers, json=game_json)
        return game_response.text
