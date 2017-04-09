import json
import status_parser
import stock_parser
import requests

status_parser = status_parser.StatusParser()
stock_parser = stock_parser.StockParser()
session = requests.Session()

email = input('Email: ')
password = input('Password: ')
game = input('Enter your game: ')

def login():
    id_url = 'http://id.marketwatch.com/auth/submitlogin.json'
    id_headers = {
        'Content-Type': 'application/json',
    }
    id_json = {
        'username': email,
        'password': password,
        'savelogin': 'true',
    }
    id_response = session.post(url=id_url, headers=id_headers, json=id_json)
    try:
        session.get(url=json.loads(id_response.text)['url'])
    except KeyError:
        print('Login failed.')
        exit(1)

def scan_status():
    status_response = session.get('http://www.marketwatch.com/game/' + game + '/portfolio/Orders')
    status_parser.feed(status_response.text)
    return status_parser.get_data()

def scan_stock(fuid):
    stock_response = session.get('http://www.marketwatch.com/game/d/trade/getpopup?fuid=' + fuid)
    stock_parser.feed(stock_response.text)
    return stock_parser.get_data()

def trade(name, shares, mode, limit):
    game_url = 'http://www.marketwatch.com/game/' + game + '/trade/submitorder'
    game_headers = {
        'Content-Type': 'application/json',
    }
    game_json = [{'Fuid': name, 'Shares': shares, 'Type': mode, 'Limit': limit}]
    game_response = session.post(url=game_url, headers=game_headers, json=game_json)
    return game_response.text

login()

status = scan_status()
print(status)
stock = scan_stock('EXCHANGETRADEDFUND-XASQ-JNUG')
print(stock)

response = trade('EXCHANGETRADEDFUND-XASQ-JNUG', '1', 'Buy', '6.75')
print(response)
