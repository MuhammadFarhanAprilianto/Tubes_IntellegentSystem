"""
Camera Handler Module
Professional camera interface with error handling and configuration
"""

import cv2
import time
from typing import Optional, Tuple
from config import Config


class CameraHandler:
    """
    Professional Camera Handler
    
    Features:
    - Multiple camera support
    - Auto-reconnection
    - Resolution configuration
    - FPS control
    - Error handling
    """
    
    def __init__(self, camera_id: int = 0, config: Config = Config):
        """
        Initialize Camera Handler
        
        Args:
            camera_id: Camera device ID (0 for default)
            config: Configuration object
        """
        self.camera_id = camera_id
        self.config = config
        self.cap = None
        self.is_opened = False
        
        # Initialize camera
        self._initialize_camera()
    
    def _initialize_camera(self) -> bool:
        """
        Initialize camera with configuration
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Initializing camera {self.camera_id}...")
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                print(f"Failed to open camera {self.camera_id}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.CAMERA_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, self.config.CAMERA_FPS)
            
            # Verify settings
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            print(f"Camera initialized successfully!")
            print(f"Resolution: {actual_width}x{actual_height}")
            print(f"FPS: {actual_fps}")
            
            self.is_opened = True
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.is_opened = False
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[cv2.Mat]]:
        """
        Read a frame from camera
        
        Returns:
            Tuple of (success, frame)
        """
        if not self.is_opened or self.cap is None:
            return False, None
        
        try:
            ret, frame = self.cap.read()
            
            if not ret:
                print("Failed to read frame from camera")
                return False, None
            
            return True, frame
            
        except Exception as e:
            print(f"Error reading frame: {e}")
            return False, None
    
    def release(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            self.is_opened = False
            print("Camera released")
    
    def reconnect(self) -> bool:
        """
        Attempt to reconnect to camera
        
        Returns:
            True if successful, False otherwise
        """
        print("Attempting to reconnect camera...")
        self.release()
        time.sleep(1)
        return self._initialize_camera()
    
    def get_camera_info(self) -> dict:
        """Get camera information"""
        if not self.is_opened or self.cap is None:
            return {}
        
        return {
            'camera_id': self.camera_id,
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(self.cap.get(cv2.CAP_PROP_FPS)),
            'backend': self.cap.getBackendName()
        }
    
    def is_available(self) -> bool:
        """Check if camera is available"""
        return self.is_opened and self.cap is not None and self.cap.isOpened()
    
    @staticmethod
    def list_available_cameras(max_cameras: int = 5) -> list:
        """
        List available cameras
        
        Args:
            max_cameras: Maximum number of cameras to check
            
        Returns:
            List of available camera IDs
        """
        available_cameras = []
        
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        
        return available_cameras
