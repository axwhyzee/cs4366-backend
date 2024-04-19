import requests
import cv2


API_URL = 'http://127.0.0.1:5000'
r = requests.post(f'{API_URL}/id_from_img/', json={'img': cv2.imread('obj_detect_backend/photo_2024-04-19 13.34.02.jpeg').tolist()})
print(r.text)
