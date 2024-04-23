import base64

from flask import Flask, request
import cv2
import numpy as np
from werkzeug.utils import secure_filename

from obj_detect_backend.detector import gen_detector
from ocr_backend.ocr import detect_text


IMG_NAME = 'img'

app = Flask(__name__)


def _pipeline(img):
    gen = gen_detector(img)

    for arr in gen:
        try:
            stop_id = detect_text(arr)
            if stop_id.isdigit() and int(stop_id) > 1000000:
                return stop_id
        except:
            pass
    return ''


@app.route('/')
def root():
    return '/'


@app.route('/id_from_img/', methods=['POST'])
def id_from_img():
    header, encoded = request.data.decode('utf-8').split(';base64,', 1)
    ext = header.split('/')[-1]
    img_path = f'{IMG_NAME}.{ext}'

    with open(img_path, "wb") as fh:
        fh.write(base64.b64decode(encoded))

    return _pipeline(img_path)


if __name__ == "__main__":
    app.run(debug=True, port=5001)