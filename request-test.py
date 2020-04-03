import requests
import sys

url = 'http://127.0.0.1:5000/'
params ={'query': sys.argv[1]}

response = requests.get(url, params)
print("China")
print(response.json())
