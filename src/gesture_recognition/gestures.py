from enum import Enum
from typing import List, Tuple

class GestureType(Enum):
    OPEN_PALM = "open_palm"
    CLOSED_FIST = "closed_fist"
    POINTING = "pointing"
    PINCH = "pinch"
    UNKNOWN = "unknown"

def calculate_finger_states(landmarks: List[Tuple[int, int, int]]) -> List[bool]:
    """
    Calculate the state (extended or not) of each finger based on hand landmarks.
    
    Args:
        landmarks (List[Tuple[int, int, int]]): List of hand landmarks.
    
    Returns:
        List[bool]: List of 5 booleans indicating if each finger is extended.
    """
    if not landmarks or len(landmarks) != 21:
        return [False] * 5

    finger_tips = [4, 8, 12, 16, 20]
    finger_bases = [2, 5, 9, 13, 17]
    thumb_base = landmarks[2]
    
    finger_states = []
    
    # Special case for thumb
    thumb_tip = landmarks[4]
    thumb_extended = thumb_tip[0] < thumb_base[0] if landmarks[17][0] < landmarks[5][0] else thumb_tip[0] > thumb_base[0]
    finger_states.append(thumb_extended)
    
    # For other fingers
    for tip, base in zip(finger_tips[1:], finger_bases[1:]):
        finger_extended = landmarks[tip][1] < landmarks[base][1]
        finger_states.append(finger_extended)
    
    return finger_states

def recognize_gesture(landmarks: List[Tuple[int, int, int]]) -> GestureType:
    """
    Recognize the gesture based on hand landmarks.
    
    Args:
        landmarks (List[Tuple[int, int, int]]): List of hand landmarks.
    
    Returns:
        GestureType: The recognized gesture.
    """
    if not landmarks:
        return GestureType.UNKNOWN
    
    finger_states = calculate_finger_states(landmarks)
    
    if all(finger_states):
        return GestureType.OPEN_PALM
    elif not any(finger_states):
        return GestureType.CLOSED_FIST
    elif finger_states[1] and not any(finger_states[2:]):
        return GestureType.POINTING
    elif finger_states[0] and finger_states[1] and not any(finger_states[2:]):
        return GestureType.PINCH
    else:
        return GestureType.UNKNOWN