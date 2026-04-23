import cv2
import json
import os
from ultralytics import YOLO

# Initialize YOLOv8 model (nano version is fast and good for student projects)
model = YOLO('yolov8n.pt')

# Define the target classes based on COCO dataset indices
# 2: car, 3: motorcycle, 5: bus, 7: truck
TARGET_CLASSES = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}

# Define weights for lane score computation
WEIGHTS = {'motorcycle': 1, 'car': 2, 'bus': 4, 'truck': 4}

def process_video(video_path):
    """Process a single video and return vehicle counts and lane score."""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return None
        
    # Initialize counts for this lane
    counts = {'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0}
    
    # Process frames (for a simple project, we can just look at a few frames or the first frame)
    # Here we process the first valid frame to get a snapshot count
    ret, frame = cap.read()
    if ret:
        # Run YOLOv8 inference on the frame
        results = model(frame, verbose=False)
        
        # Process detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class ID
                cls_id = int(box.cls[0])
                
                # Check if it's a target class
                if cls_id in TARGET_CLASSES:
                    class_name = TARGET_CLASSES[cls_id]
                    counts[class_name] += 1
                    
    cap.release()
    
    # Calculate lane score
    score = sum(counts[cls] * WEIGHTS[cls] for cls in counts)
    
    return {
        'counts': counts,
        'score': score
    }

def main():
    # Define input videos (one per lane)
    videos = [
        'lane1.mp4',
        'lane2.mp4',
        'lane3.mp4',
        'lane4.mp4'
    ]
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    results = {}
    
    print("Starting traffic analysis...")
    
    for i, video in enumerate(videos, 1):
        lane_name = f'lane_{i}'
        print(f"Processing {lane_name} ({video})...")
        
        # In a real scenario, these files would exist. 
        # For the script to run without errors if files are missing, we handle it gracefully.
        if os.path.exists(video):
            lane_data = process_video(video)
            if lane_data:
                results[lane_name] = lane_data
        else:
            print(f"Warning: {video} not found. Skipping.")
            # Add dummy data for demonstration if video is missing
            results[lane_name] = {
                'counts': {'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0},
                'score': 0,
                'note': 'Video file not found'
            }
            
    # Save results to JSON
    output_path = 'output/traffic_data.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\nAnalysis complete! Results saved to {output_path}")
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
