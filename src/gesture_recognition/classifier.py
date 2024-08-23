from typing import List, Tuple, Optional
from .gestures import GestureType, recognize_gesture

class GestureClassifier:
    def __init__(self):
        self.current_gesture: GestureType = GestureType.UNKNOWN
        self.gesture_history: List[GestureType] = []
        self.history_size: int = 5

    def classify_gesture(self, landmarks: Optional[List[Tuple[int, int, int]]]) -> GestureType:
        """
        Classify the current gesture based on hand landmarks.
        
        Args:
            landmarks (Optional[List[Tuple[int, int, int]]]): List of hand landmarks.
        
        Returns:
            GestureType: The classified gesture.
        """
        if landmarks is None:
            new_gesture = GestureType.UNKNOWN
        else:
            new_gesture = recognize_gesture(landmarks)
        
        self.gesture_history.append(new_gesture)
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        # Use the most common gesture in recent history to reduce jitter
        gesture_counts = {gesture: self.gesture_history.count(gesture) for gesture in GestureType}
        self.current_gesture = max(gesture_counts, key=gesture_counts.get)
        
        return self.current_gesture

    def get_current_gesture(self) -> GestureType:
        """
        Get the current classified gesture.
        
        Returns:
            GestureType: The current gesture.
        """
        return self.current_gesture