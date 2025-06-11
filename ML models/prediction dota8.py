import cv2
from ultralytics import YOLO
import numpy as np

# Load your trained model
model = YOLO("runs/obb/train6/weights/best.pt")  # Ensure this is YOLO-OBB compatible

# Image path
img_path = "try deep/p1.jpg"  # Change to your image

# Run prediction
results = model.predict(source=img_path, imgsz=1024, conf=0.25)

# Load original image
img = cv2.imread(img_path)

# Draw oriented bounding boxes
for r in results:
    for box in r.obb.xyxyxyxy:  # OBB corners: shape (N, 8)
        box = box.cpu().numpy().astype(int)
        pts = box.reshape(-1, 1, 2)
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

# Show the image
cv2.imshow("Prediction", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
