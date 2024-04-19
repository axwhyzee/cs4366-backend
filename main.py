from flask import Flask, request
import cv2
import numpy as np

from obj_detect_backend.detector import gen_detector
from ocr_backend.ocr import detect_text


app = Flask(__name__)

def pipeline(img):
    cv2.imwrite('new.png', np.array(img))
    gen = gen_detector('new.png')

    for arr in gen:
        try:
            stop_id = detect_text(arr)
            if stop_id.isdigit() and int(stop_id) > 1000000:
                return stop_id
        except:
            pass
    return 'No ID found'


@app.route('/')
def root():
    return '/'


@app.route('/id_from_img/', methods=['POST'])
def id_from_img():
    img = request.json.get('img')

    if not img:
        return 'No image received'
    return pipeline(img)


if __name__ == "__main__":
    app.run(debug=True)