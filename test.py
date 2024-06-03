import requests

BASE_URL = "http://127.0.0.1:5000/"

data = [
    {"likes": 34, "name": "Flask Tutorial", "views": 100},
    {"likes": 213, "name": "Github", "views": 343},
    {"likes": 923, "name": "School video", "views": 3243},
]

for i in range(len(data)):
    response = requests.put(BASE_URL + "video/" + str(i), data[i])
    print(response.json())

response = requests.put(
    BASE_URL + "video/83", {"name": "hi hello", "views": 92, "likes": 34}
)
input()
response = requests.patch(BASE_URL + "video/2", {"views": 99, "likes": 101})
print(response.json())
