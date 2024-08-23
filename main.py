import cv2
import pyautogui
from src.hand_tracking import HandDetector, draw_hand_landmarks, draw_hand_position
from src.gesture_recognition import GestureClassifier
from src.mouse_control import MouseController

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    
    # Initialize modules
    hand_detector = HandDetector()
    gesture_classifier = GestureClassifier()
    mouse_controller = MouseController((screen_width, screen_height))
    
    while True:
        # Read frame from camera
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame")
            break
        
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Detect hands and get landmarks
        frame, hand_landmarks = hand_detector.find_hands(frame)
        
        if hand_landmarks:
            # We'll use the first detected hand
            landmarks = hand_landmarks[0]
            
            # Classify gesture
            gesture = gesture_classifier.classify_gesture(landmarks)
            
            # Get hand position (using the middle finger tip as reference)
            hand_position = landmarks[9][:2]  # Middle finger MCP joint
            
            # Handle the gesture
            mouse_controller.handle_gesture(gesture, hand_position, frame.shape[1::-1])
            
            # Visualize
            frame = draw_hand_landmarks(frame, [landmarks])
            frame = draw_hand_position(frame, hand_position)
            
            # Display gesture
            cv2.putText(frame, f"Gesture: {gesture.name}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the frame
        cv2.imshow('Gesture Mouse Control', frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()