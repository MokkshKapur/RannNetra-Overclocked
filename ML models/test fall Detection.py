from inference_sdk import InferenceHTTPClient
import cv2

# Initialize Roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ExdTmiH9EHSp4DYnRxys"
)

# Load the image
image_path = 'try deep/8.jpg'
image = cv2.imread(image_path)

# Run inference
result = CLIENT.infer(image_path, model_id="fall_detection-8vxyk/2")

# Analyze and draw
for prediction in result['predictions']:
    x = int(prediction['x'])
    y = int(prediction['y'])
    w = int(prediction['width'])
    h = int(prediction['height'])
    class_name = prediction['class']

    # Bounding box coords
    x1 = int(x - w / 2)
    y1 = int(y - h / 2)
    x2 = int(x + w / 2)
    y2 = int(y + h / 2)

    # Simple classification based on aspect ratio
    aspect_ratio = w / h
    if aspect_ratio > 1.3:
        fall_type = "Prone Position"
        color = (0, 0, 255)  # Red for prone
    else:
        fall_type = "Normal Fall"
        color = (0, 255, 0)  # Green for normal

    label = f"{class_name} - {fall_type}"

    # Draw box and label
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, color, 2)

# Show the image
cv2.imshow("Fall Classification", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
