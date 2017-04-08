import requests

game = input('Enter your game: ')

cookie = input('Enter your cookie: ')

url = 'http://www.marketwatch.com/game/' + game + '/trade/submitorder'
headers = {
    'Content-Type': 'application/json',
    'Cookie': cookie,
}
json = [{"Fuid": "EXCHANGETRADEDFUND-XASQ-JNUG", "Shares": "1", "Type": "Buy", "Term": "Cancelled"}]

r = requests.post(url=url, headers=headers, json=json)
print(r.text)
