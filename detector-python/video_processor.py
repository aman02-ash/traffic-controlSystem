import cv2
import threading
import time
import queue
from ultralytics import YOLO

class VideoProcessor:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.lanes = {}
        self.running = False
        self.lock = threading.Lock()
        # Class IDs for YOLOv8: car: 2, motorcycle: 3, bus: 5, truck: 7
        self.target_classes = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
        self.weights = {'car': 2, 'motorcycle': 1, 'bus': 5, 'truck': 6}

    def start_lane(self, lane_id, video_path):
        with self.lock:
            if lane_id in self.lanes:
                self.lanes[lane_id]['active'] = False
            
            self.lanes[lane_id] = {
                'video_path': video_path,
                'counts': {'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0},
                'score': 0,
                'current_frame': None,
                'active': True,
                'queue': queue.Queue(maxsize=10)
            }
        
        thread = threading.Thread(target=self._process_video, args=(lane_id,))
        thread.daemon = True
        thread.start()

    def _process_video(self, lane_id):
        cap = cv2.VideoCapture(self.lanes[lane_id]['video_path'])
        frame_count = 0
        
        while self.lanes[lane_id]['active']:
            ret, frame = cap.read()
            if not ret:
                # Loop video for demo purposes or restart if needed
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame_count += 1
            # Process every 5th frame to optimize resource usage
            if frame_count % 5 != 0:
                continue

            # Run YOLOv8 inference
            results = self.model(frame, verbose=False, conf=0.25)[0]
            
            counts = {'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0}
            
            # Process detections
            for box in results.boxes:
                cls_id = int(box.cls[0])
                if cls_id in self.target_classes:
                    label = self.target_classes[cls_id]
                    counts[label] += 1
                    
                    # Draw bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Calculate score
            score = sum(counts[cls] * self.weights[cls] for cls in counts)
            
            # Update lane data
            with self.lock:
                self.lanes[lane_id]['counts'] = counts
                self.lanes[lane_id]['score'] = score
                
                # Encode frame for streaming
                _, buffer = cv2.imencode('.jpg', frame)
                self.lanes[lane_id]['current_frame'] = buffer.tobytes()

        cap.release()

    def get_lane_data(self):
        data = {}
        with self.lock:
            for lane_id, info in self.lanes.items():
                data[lane_id] = {
                    'counts': info['counts'],
                    'score': info['score']
                }
        return data

    def get_frame(self, lane_id):
        with self.lock:
            if lane_id in self.lanes:
                return self.lanes[lane_id]['current_frame']
        return None