import requests

url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"

querystring = {"from":"USD","to":"EUR","amount":"750"}

headers = {
	"X-RapidAPI-Key": "8f58b72c8bmshfd6ad24797b63ccp1efd77jsnfe70d5b7f4c7",
	"X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
