from urllib import response
import requests

url = 'https://xkcd.com/info.0.json'

response = requests.get(url)
print(response.json()["num"])
print(response.json()[""])