import requests

url = "http://127.0.0.1:8000/predict"
data = {"features": [4,5,1,1,1,2015,7,31,0,-1.011865674,1.071317226,3,0,1,1,0,0,0]}  


response = requests.post(url, json=data)
print(response.json())