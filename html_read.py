import requests
from lxml import html

url = 'https://coinmarketcap.com/currencies/xrp/'
page = requests.get(url)
tree = html.fromstring(page.content)

value = (tree.xpath('/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span/text()'))
value = float (str(value[0])[1:])
print(value)
