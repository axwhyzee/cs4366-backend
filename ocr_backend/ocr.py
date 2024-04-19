# suppposed to integrate eveyrth in one fn so can easily call the API
from PIL import Image
import cv2
from google.cloud import vision


def detect_text(img):
    """Detects text in the file."""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction

    client = vision.ImageAnnotatorClient()

    # # Convert the pixels into an array using numpy
    # array = np.array(img, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(bfilter)
    new_image.save('new.png')

  # mode shld be rb for images - read binary as image files have raw binary data - need to change this to read in the pixel values which may not be rb
    with open(new_image, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

  # text_detection is the api to detect text in the image
    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print("Texts:", texts)

    stop_id = None
    for text in texts:
        if text.description.isdigit():
            stop_id = text.description
            # print(f'\n"{stop_id}"') 
            vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
            ]
            # print("bounds: {}".format(",".join(vertices)))

    if stop_id:
        return stop_id
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )