import json
import status_parser
import stock_parser
import requests

class MarketWatchAPI:
    def __init__(self):
        self.status_parser = status_parser.StatusParser()
        self.stock_parser = stock_parser.StockParser()
        self.session = requests.Session()

    def __trade(self, game, game_json):
        game_url = 'http://www.marketwatch.com/game/' + game + '/trade/submitorder'
        game_headers = {
            'Content-Type': 'application/json',
        }
        game_response = self.session.post(url=game_url, headers=game_headers, json=game_json)
        game_response = json.loads(game_response.text)
        return game_response

    def clear_orders(self, game):
        for item in self.parse_player(game)['orders']:
            self.session.get('http://www.marketwatch.com' + item)

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
        id_response = json.loads(id_response.text)
        print('Login:', id_response['result'])
        try:
            self.session.get(url=id_response['url'])
        except KeyError:
            exit(1)

    def parse_player(self, game):
        status_response = self.session.get('http://www.marketwatch.com/game/' + game + '/portfolio/Orders')
        self.status_parser.feed(status_response.text)
        data = self.status_parser.get_data()
        self.status_parser.reset()
        return data

    def parse_stock(self, symbol):
        stock_response = self.session.get('http://www.marketwatch.com/game/d/trade/getpopup?fuid=' + symbol)
        self.stock_parser.feed(stock_response.text)
        data = self.stock_parser.get_data()
        self.stock_parser.reset()
        return data

    def trade_normal(self, game, name, shares, mode, term):
        game_json = [{'Fuid': name, 'Shares': shares, 'Type': mode, 'Term': term}]
        return self.__trade(game, game_json)

    def trade_limit(self, game, name, shares, mode, term, limit):
        game_json = [{'Fuid': name, 'Shares': shares, 'Type': mode, 'Term': term, 'Limit': limit}]
        return self.__trade(game, game_json)

    def trade_stop(self, game, name, shares, mode, term, stop):
        game_json = [{'Fuid': name, 'Shares': shares, 'Type': mode, 'Term': term, 'Stop': stop}]
        return self.__trade(game, game_json)
