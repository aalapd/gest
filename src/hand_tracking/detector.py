import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, List, Optional
from mediapipe.python.solutions import drawing_utils as mp_drawing

class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def find_hands(self, image: np.ndarray) -> Tuple[np.ndarray, List[Optional[List[Tuple[int, int, int]]]]]:
        """
        Detect hands in the input image and return the processed image and landmarks.

        Args:
            image (np.ndarray): Input image in BGR format.

        Returns:
            Tuple[np.ndarray, List[Optional[List[Tuple[int, int, int]]]]]: 
                - Processed image with hand landmarks drawn
                - List of detected hand landmarks (None if no hand detected)
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        all_hand_landmarks = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    h, w, _ = image.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    landmarks.append((cx, cy, landmark.z))
                all_hand_landmarks.append(landmarks)
                
                # Draw landmarks on the image
                mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        return image, all_hand_landmarks

    def get_hand_position(self, landmarks: List[Tuple[int, int, int]], hand_index: int = 0) -> Optional[Tuple[int, int]]:
        """
        Get the position of a specific hand based on its index.

        Args:
            landmarks (List[Tuple[int, int, int]]): List of hand landmarks.
            hand_index (int): Index of the hand to get the position for (default is 0).

        Returns:
            Optional[Tuple[int, int]]: (x, y) coordinates of the hand's center, or None if not available.
        """
        if landmarks and len(landmarks) > hand_index:
            hand = landmarks[hand_index]
            if hand:
                # Use the average position of all landmarks as the hand's center
                x = int(sum(lm[0] for lm in hand) / len(hand))
                y = int(sum(lm[1] for lm in hand) / len(hand))
                return (x, y)
        return None