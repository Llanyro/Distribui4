"""import numpy

matriz1 = [[1, 2, 4, 6], [2, 3, 5, 1], [2, 3, 1, 2], [12, 3, 23, 4]]
matriz2 = [[1, 2, 2, 6], [2, 3, 5, 22], [3, 3, 1, 4], [2, 3, 3, 12]]
print(numpy.matmul(matriz1, matriz2))"""


import requests

print(requests.post(url="https://9pmvwa88yc.execute-api.us-east-1.amazonaws.com/login", data={"peticion": "getVideos"}))
