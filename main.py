import cv2 as cv
import numpy as np
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles

from handgestures import detect_gesture



# Create an HandLandmarker object
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task') #trained model used
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=1) #configuration of detector
detector = vision.HandLandmarker.create_from_options(options)

cap = cv.VideoCapture(0)  #obra la camara

while(True):
    ret, frame = cap.read()  #captura la imatge de la càmara

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) #from BGR2RGB

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    result = detector.detect(mp_image) #returns HandLandmarkerResult objects with 21 landmarks
    
    for hand_landmarks in result.hand_landmarks:   #for every landmark in result 
        drawing_utils.draw_landmarks(     #draw on frame the landmarks
            frame,
            hand_landmarks,
            vision.HandLandmarksConnections.HAND_CONNECTIONS,  #connect landmarks the correct way
            drawing_styles.get_default_hand_landmarks_style(),
            drawing_styles.get_default_hand_connections_style()
        )

        #get x,y coordenates from the top index fingertip
        gesture=detect_gesture(hand_landmarks)
        
    frame = cv.flip(frame, 1) #pantalla sense efecte mirall    
    cv.imshow("Hand controll", frame)


    
    if cv.waitKey(1) & 0xFF == ord('q'): #espera la tecla q cada 1 ms per sortir
        break


    

cap.release()     #deixa la càmara lliure
detector.close()
cv.destroyAllWindows()
