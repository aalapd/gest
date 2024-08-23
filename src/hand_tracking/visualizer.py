import cv2
import numpy as np
from typing import List, Tuple, Optional

def draw_hand_landmarks(image: np.ndarray, landmarks: List[Optional[List[Tuple[int, int, int]]]]) -> np.ndarray:
    """
    Draw hand landmarks on the input image.

    Args:
        image (np.ndarray): Input image to draw on.
        landmarks (List[Optional[List[Tuple[int, int, int]]]]): List of detected hand landmarks.

    Returns:
        np.ndarray: Image with hand landmarks drawn.
    """
    for hand_landmarks in landmarks:
        if hand_landmarks:
            for lm in hand_landmarks:
                cv2.circle(image, (lm[0], lm[1]), 5, (0, 255, 0), cv2.FILLED)
    
    return image

def draw_hand_position(image: np.ndarray, position: Optional[Tuple[int, int]]) -> np.ndarray:
    """
    Draw the hand position on the input image.

    Args:
        image (np.ndarray): Input image to draw on.
        position (Optional[Tuple[int, int]]): (x, y) coordinates of the hand's center.

    Returns:
        np.ndarray: Image with hand position drawn.
    """
    if position:
        cv2.circle(image, position, 10, (255, 0, 0), cv2.FILLED)
    
    return image