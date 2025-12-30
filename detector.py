"""
Object Detection Module using YOLOv8
Professional implementation with error handling and optimization
"""

import cv2
import time
import numpy as np
from ultralytics import YOLO
from typing import Tuple, List, Optional
from config import Config


class ObjectDetector:
    """
    Professional Object Detector using YOLOv8
    
    Features:
    - Real-time object detection
    - FPS counter
    - Configurable confidence threshold
    - GPU acceleration support
    - Error handling and logging
    """
    
    def __init__(self, model_path: Optional[str] = None, config: Config = Config):
        """
        Initialize the Object Detector
        
        Args:
            model_path: Path to YOLO model file
            config: Configuration object
        """
        self.config = config
        self.model_path = model_path or config.MODEL_PATH
        self.model = None
        self.class_names = []
        
        # Performance tracking
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        # Initialize model
        self._load_model()
        
    def _load_model(self):
        """Load YOLO model with error handling"""
        try:
            print(f"Loading model: {self.model_path}")
            self.model = YOLO(self.model_path)
            
            # Get class names
            self.class_names = self.model.names
            print(f"Model loaded successfully!")
            print(f"Available classes: {len(self.class_names)}")
            
            # Set device (GPU/CPU)
            if self.config.USE_GPU:
                print("Using GPU acceleration (if available)")
            else:
                print("Using CPU only")
                
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Model will be downloaded automatically on first use.")
            # Model will auto-download if not found
            self.model = YOLO(Config.MODEL_NAME)
            self.class_names = self.model.names
    
    def detect_objects(self, frame: np.ndarray) -> Tuple[np.ndarray, List]:
        """
        Detect objects in a frame
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            Tuple of (annotated_frame, detections)
        """
        if self.model is None:
            return frame, []
        
        try:
            # Run inference
            results = self.model(
                frame,
                conf=self.config.CONFIDENCE_THRESHOLD,
                iou=self.config.IOU_THRESHOLD,
                verbose=False
            )
            
            # Get detections
            detections = []
            
            for result in results:
                boxes = result.boxes
                
                for box in boxes:
                    # Extract box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.class_names[class_id]
                    
                    detection = {
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': confidence,
                        'class_id': class_id,
                        'class_name': class_name
                    }
                    detections.append(detection)
            
            # Draw annotations
            annotated_frame = self._draw_annotations(frame.copy(), detections)
            
            return annotated_frame, detections
            
        except Exception as e:
            print(f"Detection error: {e}")
            return frame, []
    
    def _draw_annotations(self, frame: np.ndarray, detections: List) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: Input frame
            detections: List of detection dictionaries
            
        Returns:
            Annotated frame
        """
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            confidence = det['confidence']
            class_name = det['class_name']
            
            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                self.config.BOX_COLOR,
                self.config.BOX_THICKNESS
            )
            
            # Prepare label
            if self.config.SHOW_CONFIDENCE:
                label = f"{class_name}: {confidence:.2f}"
            else:
                label = class_name
            
            # Get label size for background
            (label_width, label_height), baseline = cv2.getTextSize(
                label,
                self.config.FONT,
                self.config.FONT_SCALE,
                self.config.FONT_THICKNESS
            )
            
            # Draw label background
            cv2.rectangle(
                frame,
                (x1, y1 - label_height - baseline - 5),
                (x1 + label_width, y1),
                self.config.TEXT_BG_COLOR,
                -1
            )
            
            # Draw label text
            cv2.putText(
                frame,
                label,
                (x1, y1 - baseline - 5),
                self.config.FONT,
                self.config.FONT_SCALE,
                self.config.TEXT_COLOR,
                self.config.FONT_THICKNESS
            )
        
        return frame
    
    def calculate_fps(self) -> float:
        """Calculate current FPS"""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        
        if elapsed_time > 1.0:  # Update FPS every second
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()
        
        return self.fps
    
    def draw_fps(self, frame: np.ndarray) -> np.ndarray:
        """
        Draw FPS counter on frame
        
        Args:
            frame: Input frame
            
        Returns:
            Frame with FPS overlay
        """
        fps = self.calculate_fps()
        fps_text = f"FPS: {fps:.1f}"
        
        cv2.putText(
            frame,
            fps_text,
            (10, 30),
            self.config.FONT,
            self.config.FONT_SCALE,
            self.config.FPS_COLOR,
            self.config.FONT_THICKNESS
        )
        
        return frame
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            'model_path': self.model_path,
            'num_classes': len(self.class_names),
            'class_names': self.class_names,
            'confidence_threshold': self.config.CONFIDENCE_THRESHOLD
        }
