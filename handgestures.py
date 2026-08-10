import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles

import pydotool

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

pydotool.init()

def detect_gesture(hand):
    if index_up(hand):
        move_mouse(hand)

        
def index_up(hand):
    index = hand[8].y < hand[6].y
    middle = hand[12].y > hand[10].y
    ring = hand[16].y > hand[14].y
    pinky = hand[20].y > hand[18].y
    
    return index and middle and ring and pinky


def move_mouse(hand):
    x_i = hand[8].x
    y_i = hand[8].y

    x_screen = int((1 - x_i) * SCREEN_WIDTH)
    y_screen = int(y_i * SCREEN_HEIGHT)

    pydotool.mouse_move((x_screen, y_screen), True)
    
    
