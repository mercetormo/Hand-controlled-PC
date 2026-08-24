import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles

import pydotool

import math

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

prev_x = 0
prev_y = 0

SMOOTHING = 5
DEAD_ZONE = 2

pinching = False

X_MIN = 0.2
X_MAX = 0.8

Y_MIN = 0.2
Y_MAX = 0.8

pydotool.init()

def detect_gesture(hand):
    if index_up(hand):
        move_mouse(hand)
    elif index_thumb(hand):
        click(hand)

        
def index_up(hand):
    index = hand[8].y < hand[6].y
    middle = hand[12].y > hand[10].y
    ring = hand[16].y > hand[14].y
    pinky = hand[20].y > hand[18].y
    thumb = hand[4].y > hand[11].y
    
    return index and middle and ring and pinky and thumb


def index_thumb(hand):
    index = hand[8].y < hand[6].y
    middle = hand[12].y > hand[10].y
    ring = hand[16].y > hand[14].y
    pinky = hand[20].y > hand[18].y
    thumb = hand[4].y < hand[11].y

    return index and middle and ring and pinky and thumb


def move_mouse(hand):
    global prev_x, prev_y
    
    x_i = hand[8].x
    y_i = hand[8].y

    # Limita el moviment a una zona més petita de la càmera
    x_i = max(X_MIN, min(x_i, X_MAX))
    y_i = max(Y_MIN, min(y_i, Y_MAX))

    # Converteix aquesta zona a un rang 0-1
    x_norm = (x_i - X_MIN) / (X_MAX - X_MIN)
    y_norm = (y_i - Y_MIN) / (Y_MAX - Y_MIN)

    target_x = int((1 - x_norm) * SCREEN_WIDTH)
    target_y = int(y_norm * SCREEN_HEIGHT)

    if (abs(target_x - prev_x) < DEAD_ZONE and abs(target_y - prev_y) < DEAD_ZONE):
        return

    x_screen = prev_x + (target_x - prev_x) / SMOOTHING
    y_screen = prev_y + (target_y - prev_y) / SMOOTHING

    pydotool.mouse_move((int(x_screen), int(y_screen)), True)

    prev_x = x_screen
    prev_y = y_screen

def click(hand):
    global pinching
    
    dx= hand[4].y-hand[8].y
    dy= hand[4].x-hand[8].x

    distance = math.sqrt(dx**2 + dy**2)

    if distance <0.05:
        pydotool.left_click()
        pinching=True

    elif distance > 0.07:
        pinching=False
    
    
