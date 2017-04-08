import json
import requests

email = input('Email: ')
password = input('Password: ')
session = requests.Session()

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
    session.get(url=json.loads(id_response.text)["url"])
except KeyError:
    print("Login failed.")
    exit(1)


game = input('Enter your game: ')
game_url = 'http://www.marketwatch.com/game/' + game + '/trade/submitorder'
game_headers = {
    'Content-Type': 'application/json',
}

game_json = [{"Fuid": "EXCHANGETRADEDFUND-XASQ-JNUG", "Shares": "1", "Type": "Buy"}]
game_response = session.post(url=game_url, headers=game_headers, json=game_json)
print(game_response.text)
