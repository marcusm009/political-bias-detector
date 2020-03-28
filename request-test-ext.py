import requests
import sys

params ={'query': sys.argv[2]}

response = requests.get(sys.argv[1], params)
print(response.json())
