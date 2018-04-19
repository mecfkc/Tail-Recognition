#File for testing network
# USAGE
# python test_network.py --image test_rr.png

from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2

dimensions = 28

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
orig = image.copy()

# pre-process the image for classification
image = cv2.resize(image, (dimensions, dimensions))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model("aircraft_detection.model")

# classify the input image
(red_rectangle, red_triangle, blue_rectangle, blue_triangle, yellow_rectangle, yellow_triangle) = model.predict(image)[0]
probability = max([red_rectangle, red_triangle, blue_rectangle, blue_triangle, yellow_rectangle, yellow_triangle])
print(probability)
print(red_rectangle)
print(red_triangle)
print(blue_rectangle)
print(blue_triangle)
print(yellow_rectangle)
print(yellow_triangle)

if probability == red_rectangle:
	label = "red_rectangle"
if probability == red_triangle:
	label = "red_triangle"
if probability == blue_rectangle:
	label = "blue_rectangle"
if probability == blue_triangle:
	label = "blue_triangle"
if probability == yellow_rectangle:
	label = "yellow_rectangle"
if probability == yellow_triangle:
	label = "yellow_rectangle"

# build the label
label = "{}: {:.2f}%".format(label, probability * 100)

# draw the label on the image
output = imutils.resize(orig, width=400)
cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
	0.7, (0, 0, 0), 2)

# show the output image
cv2.imshow("Output", output)
cv2.waitKey(0)
