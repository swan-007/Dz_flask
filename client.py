import requests

# url = "http://127.0.0.1:5000/api"
# response = requests.post(url, json={'heading': 'Статья',
#                                     'description': 'Описание',
#                                     'user_id': 1})

response = requests.get('http://127.0.0.1:5000/api/2')

print(response.status_code)
print(response.text)


# response = requests.patch('http://127.0.0.1:5000/api/1', json={'user_id': 1,
#                                                                })
#
# print(response.status_code)
# print(response.text)


# response = requests.delete("http://127.0.0.1:5000/api/1")
#
# print(response.status_code)
# print(response.text)
