from inference_sdk import InferenceHTTPClient
import cv2
import os

# Setup
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ExdTmiH9EHSp4DYnRxys"
)

# Safe path handling
image_path = os.path.abspath(r'C:\Users\user\PycharmProjects\Human-Fall-Detection-Yolov12-Mediapipe\try deep\4.jpeg')
image = cv2.imread(image_path)

# Error check
if image is None:
    raise FileNotFoundError(f"Could not read image at: {image_path}")

# Inference
result = CLIENT.infer(image_path, model_id="final-missiles/2")

# Draw results
for prediction in result['predictions']:
    x, y = int(prediction['x']), int(prediction['y'])
    w, h = int(prediction['width']), int(prediction['height'])
    x1, y1 = x - w // 2, y - h // 2
    x2, y2 = x + w // 2, y + h // 2
    label = prediction['class']

    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# Show output
cv2.imshow("Rocket Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
