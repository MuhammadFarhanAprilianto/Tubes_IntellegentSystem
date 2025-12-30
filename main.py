"""
Real-Time Object Detection System
Professional implementation with YOLOv8 and OpenCV

Author: Professional Python Developer
Description: Detects objects in real-time from camera feed using YOLOv8
"""

import cv2
import sys
import argparse
from datetime import datetime
from detector import ObjectDetector
from camera_handler import CameraHandler
from config import Config


class ObjectDetectionSystem:
    """Main Object Detection System"""
    
    def __init__(self, camera_id: int = 0):
        """
        Initialize the detection system
        
        Args:
            camera_id: Camera device ID
        """
        print("=" * 60)
        print("OBJECT DETECTION SYSTEM - YOLOv8")
        print("=" * 60)
        
        # Create necessary directories
        Config.create_directories()
        
        # Initialize components
        self.camera = CameraHandler(camera_id, Config)
        self.detector = ObjectDetector(config=Config)
        self.is_running = False
        
        # Video writer for recording
        self.video_writer = None
        
        # Display system info
        self._display_system_info()
    
    def _display_system_info(self):
        """Display system information"""
        print("\n[SYSTEM INFORMATION]")
        
        # Camera info
        camera_info = self.camera.get_camera_info()
        if camera_info:
            print(f"Camera ID: {camera_info['camera_id']}")
            print(f"Resolution: {camera_info['width']}x{camera_info['height']}")
            print(f"FPS: {camera_info['fps']}")
            print(f"Backend: {camera_info['backend']}")
        
        # Model info
        model_info = self.detector.get_model_info()
        print(f"\nModel: {model_info['model_path']}")
        print(f"Classes: {model_info['num_classes']}")
        print(f"Confidence Threshold: {model_info['confidence_threshold']}")
        
        print("\n[CONTROLS]")
        print("Press 'q' or 'ESC' to quit")
        print("Press 's' to save current frame")
        print("Press 'r' to toggle recording")
        print("Press 'i' to show detection info")
        print("=" * 60)
        print()
    
    def _save_frame(self, frame, detections):
        """Save current frame with detections"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{Config.OUTPUT_DIR}/detection_{timestamp}.jpg"
        
        cv2.imwrite(filename, frame)
        print(f"Frame saved: {filename}")
        print(f"Detections: {len(detections)} objects")
    
    def _toggle_recording(self, frame):
        """Toggle video recording"""
        if self.video_writer is None:
            # Start recording
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{Config.OUTPUT_DIR}/recording_{timestamp}.mp4"
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = Config.CAMERA_FPS
            frame_size = (frame.shape[1], frame.shape[0])
            
            self.video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
            print(f"Recording started: {filename}")
        else:
            # Stop recording
            self.video_writer.release()
            self.video_writer = None
            print("Recording stopped")
    
    def _show_detection_info(self, detections):
        """Display detection information"""
        print("\n" + "=" * 60)
        print(f"CURRENT DETECTIONS: {len(detections)}")
        print("=" * 60)
        
        if detections:
            for i, det in enumerate(detections, 1):
                print(f"{i}. {det['class_name']} - Confidence: {det['confidence']:.2%}")
        else:
            print("No objects detected")
        
        print("=" * 60 + "\n")
    
    def run(self):
        """Run the object detection system"""
        if not self.camera.is_available():
            print("ERROR: Camera not available!")
            return
        
        self.is_running = True
        print("Starting detection... (Press 'q' to quit)\n")
        
        try:
            while self.is_running:
                # Read frame from camera
                ret, frame = self.camera.read_frame()
                
                if not ret or frame is None:
                    print("Failed to read frame. Attempting reconnection...")
                    if not self.camera.reconnect():
                        print("Could not reconnect to camera. Exiting...")
                        break
                    continue
                
                # Detect objects
                annotated_frame, detections = self.detector.detect_objects(frame)
                
                # Draw FPS if enabled
                if Config.SHOW_FPS:
                    annotated_frame = self.detector.draw_fps(annotated_frame)
                
                # Add detection count
                detection_text = f"Objects: {len(detections)}"
                cv2.putText(
                    annotated_frame,
                    detection_text,
                    (10, 60),
                    Config.FONT,
                    Config.FONT_SCALE,
                    Config.FPS_COLOR,
                    Config.FONT_THICKNESS
                )
                
                # Record if enabled
                if self.video_writer is not None:
                    self.video_writer.write(annotated_frame)
                    # Show recording indicator
                    cv2.circle(annotated_frame, (annotated_frame.shape[1] - 30, 30), 10, (0, 0, 255), -1)
                
                # Display frame
                cv2.imshow(Config.WINDOW_NAME, annotated_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:  # 'q' or ESC
                    print("\nStopping detection...")
                    break
                elif key == ord('s'):  # Save frame
                    self._save_frame(annotated_frame, detections)
                elif key == ord('r'):  # Toggle recording
                    self._toggle_recording(annotated_frame)
                elif key == ord('i'):  # Show info
                    self._show_detection_info(detections)
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        except Exception as e:
            print(f"\nError during detection: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        
        if self.video_writer is not None:
            self.video_writer.release()
        
        self.camera.release()
        cv2.destroyAllWindows()
        
        print("System shutdown complete")
        print("=" * 60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Real-Time Object Detection System using YOLOv8"
    )
    parser.add_argument(
        '--camera',
        type=int,
        default=0,
        help='Camera device ID (default: 0)'
    )
    parser.add_argument(
        '--list-cameras',
        action='store_true',
        help='List available cameras'
    )
    
    args = parser.parse_args()
    
    # List cameras if requested
    if args.list_cameras:
        print("Scanning for available cameras...")
        cameras = CameraHandler.list_available_cameras()
        print(f"Available cameras: {cameras}")
        return
    
    # Run detection system
    system = ObjectDetectionSystem(camera_id=args.camera)
    system.run()


if __name__ == "__main__":
    main()
