import json
import parser
import requests

custom_parser = parser.CustomParser()
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

def scan():
    data_response = session.get('http://www.marketwatch.com/game/' + game + '/portfolio/Orders')
    custom_parser.feed(data_response.text)
    return custom_parser.get_data()

def trade(name, shares, mode, limit):
    game_url = 'http://www.marketwatch.com/game/' + game + '/trade/submitorder'
    game_headers = {
        'Content-Type': 'application/json',
    }
    game_json = [{'Fuid': name, 'Shares': shares, 'Type': mode, 'Limit': limit}]
    game_response = session.post(url=game_url, headers=game_headers, json=game_json)
    return game_response.text

login()

data = scan()
print(data['Buying Power'])

response = trade('EXCHANGETRADEDFUND-XASQ-JNUG', '1', 'Buy', '6.75')
print(response)
