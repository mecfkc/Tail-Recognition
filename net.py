#USAGE
# python net.py --dataset images

from random import shuffle
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras import backend as K
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from imutils import paths
from keras.optimizers import SGD
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os

dimensions = 28 # both height and width of images
classes = 6 # current classes: red rectangle, red triangle, blue rectangle, blue triangle, yellow rectangle, yellow triangle
data = []
labels = []

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="path to input dataset")
args = vars(ap.parse_args())

# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)

# loop over the input images
for imagePath in imagePaths:
	# load the image, pre-process it, and store it in the data list
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (dimensions, dimensions))
	image = img_to_array(image)
	data.append(image)

	# extract the class label from the image path and update the
	# labels list
	# labels include: red_rectangle, red_triangle, blue_rectangle, blue_triangle, yellow_rectangle, yellow_triangle
	label = imagePath.split(os.path.sep)[-2]
	if label == "red_rectangle":
		label = 0
	elif label == "red_triangle":
		label = 1
	elif label == "blue_rectangle":
		label = 2
	elif label == "blue_triangle":
		label = 3
	elif label == "yellow_rectangle":
		label = 4
	elif label == "yellow_triangle":
		label = 5
	labels.append(label)

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

data_mix = np.array(data)
labels_mix = np.array(labels)

num_images = 600
count = 0

for count_images in range(0, num_images):
	if count == 100:
		count = 0

	if count % 6 == 0:
		data_mix[count_images] = data[count]
		labels_mix[count_images] = label[count]
	elif count % 6 == 1:
		data_mix[count_images] = data[count+100]
		labels_mix[count_images] = label[count+100]
	elif count % 6 == 2:
		data_mix[count_images] = data[count+200]
		labels_mix[count_images] = label[count+200]
	elif count % 6 == 3:
		data_mix[count_images] = data[count+300]
		labels_mix[count_images] = label[count+300]
	elif count % 6 == 4:
		data_mix[count_images] = data[count+400]
		labels_mix[count_images] = label[count+400]
	else:
		data_mix[count_images] = data[count+500]
		labels_mix[count_images] = label[count+500]
	count+= 1

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.25, random_state=42)

# convert the labels from integers to vectors
trainY = to_categorical(trainY, num_classes=classes)
testY = to_categorical(testY, num_classes=classes)

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

print("Compiling model")
# input 28x28 images
model = Sequential()

# first set of CONV => RELU => POOL layers
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(dimensions, dimensions, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# second set of CONV => RELU => POOL layers
model.add(Conv2D(50, (5, 5), padding="same"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# first (and only) set of FC => RELU layers
model.add(Flatten())
model.add(Dense(500))
model.add(Activation("relu"))

# softmax classifier
model.add(Dense(classes))
model.add(Activation("softmax"))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

# train the network
print("Training network")
model.fit_generator(aug.flow(trainX, trainY, batch_size=5),
validation_data=(testX, testY), steps_per_epoch=len(trainX) // 5,
epochs=25, verbose=1)

model.save("aircraft_detection.model")
