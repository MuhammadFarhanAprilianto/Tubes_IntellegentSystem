"""
Configuration file for Object Detection System
"""

import os

class Config:
    """Configuration class for object detection parameters"""
    
    # Model Configuration
    MODEL_NAME = "yolov8n.pt"  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
    MODEL_PATH = os.path.join("models", MODEL_NAME)
    
    # Detection Parameters
    CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for detection (0.0 - 1.0)
    IOU_THRESHOLD = 0.45  # Intersection over Union threshold for NMS
    
    # Camera Configuration
    CAMERA_ID = 0  # Default camera (0 for built-in, 1+ for external)
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    CAMERA_FPS = 30
    
    # Display Configuration
    SHOW_FPS = True
    SHOW_CONFIDENCE = True
    SHOW_LABELS = True
    WINDOW_NAME = "Object Detection - YOLOv8"
    
    # Colors (BGR format for OpenCV)
    BOX_COLOR = (0, 255, 0)  # Green
    TEXT_COLOR = (255, 255, 255)  # White
    TEXT_BG_COLOR = (0, 255, 0)  # Green
    FPS_COLOR = (0, 255, 255)  # Yellow
    
    # Font Configuration
    FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6
    FONT_THICKNESS = 2
    BOX_THICKNESS = 2
    
    # Recording Configuration
    ENABLE_RECORDING = False
    OUTPUT_DIR = "outputs"
    SAVE_DETECTIONS = False
    
    # Performance
    USE_GPU = True  # Set to False to use CPU only
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        os.makedirs("models", exist_ok=True)
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
