import pyautogui
from typing import Tuple, Optional
from ..gesture_recognition import GestureType

class MouseController:
    def __init__(self, screen_size: Tuple[int, int], smoothing_factor: float = 0.25):
        self.screen_width, self.screen_height = screen_size
        self.smoothing_factor = smoothing_factor
        self.last_x, self.last_y = pyautogui.position()
        pyautogui.FAILSAFE = False  # Disable fail-safe

    def move_mouse(self, hand_position: Tuple[int, int], frame_size: Tuple[int, int]):
        """
        Move the mouse based on the hand position.
        
        Args:
            hand_position (Tuple[int, int]): The (x, y) position of the hand.
            frame_size (Tuple[int, int]): The (width, height) of the camera frame.
        """
        frame_width, frame_height = frame_size
        hand_x, hand_y = hand_position

        # Map hand position to screen coordinates
        screen_x = int((hand_x / frame_width) * self.screen_width)
        screen_y = int((hand_y / frame_height) * self.screen_height)

        # Apply smoothing
        smooth_x = int(self.last_x + (screen_x - self.last_x) * self.smoothing_factor)
        smooth_y = int(self.last_y + (screen_y - self.last_y) * self.smoothing_factor)

        # Move the mouse
        pyautogui.moveTo(smooth_x, smooth_y)

        # Update last position
        self.last_x, self.last_y = smooth_x, smooth_y

    def perform_click(self, click_type: str = 'left'):
        """
        Perform a mouse click.
        
        Args:
            click_type (str): The type of click ('left' or 'right').
        """
        if click_type == 'left':
            pyautogui.click()
        elif click_type == 'right':
            pyautogui.rightClick()

    def handle_gesture(self, gesture: GestureType, hand_position: Optional[Tuple[int, int]], frame_size: Tuple[int, int]):
        """
        Handle the recognized gesture and perform corresponding mouse action.
        
        Args:
            gesture (GestureType): The recognized gesture.
            hand_position (Optional[Tuple[int, int]]): The (x, y) position of the hand, if available.
            frame_size (Tuple[int, int]): The (width, height) of the camera frame.
        """
        if hand_position:
            if gesture == GestureType.OPEN_PALM:
                self.move_mouse(hand_position, frame_size)
            elif gesture == GestureType.PINCH:
                self.perform_click('left')
            elif gesture == GestureType.CLOSED_FIST:
                self.perform_click('right')
        # Note: We don't handle POINTING here as it doesn't map to a specific mouse action