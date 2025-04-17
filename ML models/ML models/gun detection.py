from inference_sdk import InferenceHTTPClient
import cv2
import os

# Initialize Roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ExdTmiH9EHSp4DYnRxys"
)

# Image path (make sure this is correct)
image_path = r'C:\Users\user\PycharmProjects\Human-Fall-Detection-Yolov12-Mediapipe\try deep\20.jpg'
image = cv2.imread(image_path)

# Error check
if image is None:
    raise FileNotFoundError(f"Could not read image at: {image_path}")

# Run inference
result = CLIENT.infer(image_path, model_id="threat-detection-xoido/1")

# Draw predictions
for pred in result['predictions']:
    x, y = int(pred['x']), int(pred['y'])
    w, h = int(pred['width']), int(pred['height'])
    class_name = pred['class']

    x1, y1 = x - w // 2, y - h // 2
    x2, y2 = x + w // 2, y + h // 2

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, class_name, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Show output
cv2.imshow("Threat Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
