from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

#path to trained keras model
MODEL_PATH = "aircraft_detection.model"

dimensions = 28

#load trained model
print("Loading model")
model = load_model(MODEL_PATH)

#Loading video feed
print("Starting video stream")
vs = VideoStream(0).start()
time.sleep(2.0)

while True:
    #read and resize each frame
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    #prepare image to be classified
    image = cv2.resize(frame, (dimensions, dimensions))
    image = image.astype("float")/255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    #classify image
    (red_rectangle, red_triangle, blue_rectangle, blue_triangle, yellow_rectangle, yellow_triangle) = model.predict(image)[0]
    probability = max([red_rectangle, red_triangle, blue_rectangle, blue_triangle, yellow_rectangle, yellow_triangle])


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

    label = "{}: {:.2f}%".format(label, probability * 100)
    frame = cv2.putText(frame, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 0, 0), 2)

    #output frame
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

print("Closing")
cv2.destroyAllWindows()
vs.stop()


"""
This sort of check may need added

#total consecutive frames tennis ball recognized
TOTAL_CONSEC = 0
#how many frames until confirming tennis tennis_ball
TOTAL_THRESH = 20
#tennis ball spotted
TENNIS_BALL = False

        
    #if tennis ball is detected
    if tennis_ball > not_tennis_ball:
        label = "tennis_ball"
        probability = tennis_ball
        TOTAL_CONSEC += 1

    #check if spotted in enough consecutive frames
    if not TENNIS_BALL and TOTAL_CONSEC >= TOTAL_THRESH:
        TENNIS_BALL = True

        #processing, math, calling other functions here

    else:
        TOTAL_CONSEC = 0
        TENNIS_BALL = False
"""
