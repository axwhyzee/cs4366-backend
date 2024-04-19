from ultralytics import YOLO
from matplotlib import pyplot as plt
import cv2

from ocr_backend.ocr import detect_text


model = YOLO("obj_detect_backend/best.pt")

def gen_detector(file):
    img = cv2.imread(file)
    results = model(file)

    # Extract bounding boxes, classes, names, and confidences
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    # Iterate through the results
    for box, cls, conf in zip(boxes, classes, confidences):
        x1, y1, x2, y2 = box

        img_cropped = img[int(y1):int(y2), int(x1):int(x2)]
        yield img_cropped