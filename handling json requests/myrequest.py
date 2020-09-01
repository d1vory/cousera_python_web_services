import requests
import ast
import base64
import json

# base_url = 'https://datasend.webpython.graders.eldf.ru/'
#
# url = base_url+'submissions/1/'
#
# headers = {'Authorization' : 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'  }
#
# r = requests.post(url, headers=headers)
#
#
# dict_str = r.content.decode("UTF-8")
# kek = ast.literal_eval(dict_str)
# print(kek)
#
# 'Z2FsY2hvbm9rOmt0b3RhbWE='
#
# url2 = base_url + kek['path']
#
# r2 = requests.put(url2, headers = {'Authorization' : 'Basic Z2FsY2hvbm9rOmt0b3RhbWE=' })
# print(r2.text)

url = 'http://127.0.0.1:8000/api/v1/goods/'
data = json.dumps({"title": 127, "description": "The number 1 cheese in the world!", "price": 100})

r = requests.post(url, data=data, headers ={'content-type':'application/json'})
print(r)
# url = 'http://127.0.0.1:8000/api/v1/goods/8/reviews/'
# data = json.dumps({
#         "text": "Best. Cheese. Ever.",
#         "grade": 3
#        })
#
# r = requests.post(url, data=data, headers ={'content-type':'application/json'})

# url = 'http://127.0.0.1:8000/api/v1/goods/2/'
#
# r = requests.get(url)
# print(r.text)