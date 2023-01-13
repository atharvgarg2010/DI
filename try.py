import requests

url = "https://sms77io.p.rapidapi.com/analytics"

querystring = {"p":"<REQUIRED>","label":"all","subaccounts":"only_main"}

headers = {
	"X-RapidAPI-Key": "211318f093msh161822ab1862c4cp16b818jsn2fe3668647d4",
	"X-RapidAPI-Host": "sms77io.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)