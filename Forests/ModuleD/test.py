import requests
import json

url = 'http://127.0.0.1:2/train_model'

response = requests.post(url, json={'photo_path': 'forest.jpg',
                                    'label': 2})


# with open('forest.jpg', 'rb') as file:
#     response = requests.post(url, files={'file': ('forest.jpg', file)}, params={'filename_new': 'forest'})

print(response.text)


