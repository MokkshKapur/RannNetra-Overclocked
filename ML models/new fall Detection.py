import cv2
import mediapipe as mp
import numpy as np
from inference_sdk import InferenceHTTPClient

# Roboflow Client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ExdTmiH9EHSp4DYnRxys"
)

# MediaPipe Pose Setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)
mp_drawing = mp.solutions.drawing_utils

# Load Image
image_path = 'try deep/9.jpg'
image = cv2.imread(image_path)

# Run Roboflow Inference
result = CLIENT.infer(image_path, model_id="fall_detection-8vxyk/2")

for prediction in result['predictions']:
    # Extract bounding box
    x, y, w, h = map(int, [prediction['x'], prediction['y'], prediction['width'], prediction['height']])
    x1 = max(0, int(x - w / 2))
    y1 = max(0, int(y - h / 2))
    x2 = min(image.shape[1], int(x + w / 2))
    y2 = min(image.shape[0], int(y + h / 2))

    # Crop ROI
    cropped = image[y1:y2, x1:x2]

    # Run MediaPipe Pose on cropped region
    rgb_crop = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_crop)

    fall_type = "Uncertain"
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Key points: left/right shoulder & hip
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        # Calculate shoulder-hip center line angle
        shoulder_mid = np.array([(left_shoulder.x + right_shoulder.x) / 2,
                                 (left_shoulder.y + right_shoulder.y) / 2])
        hip_mid = np.array([(left_hip.x + right_hip.x) / 2,
                            (left_hip.y + right_hip.y) / 2])
        delta = hip_mid - shoulder_mid
        angle = np.degrees(np.arctan2(delta[1], delta[0]))

        # Use angle to determine posture
        if abs(angle) < 30:  # Mostly horizontal
            fall_type = "Prone Position"
        else:
            fall_type = "Normal Fall"
    else:
        fall_type = "No pose detected"

    # Annotate original image
    label = f"{prediction['class']} - {fall_type}"
    color = (0, 0, 255) if fall_type == "Prone Position" else (0, 255, 0)
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

# Display result
cv2.imshow("Fall Classification with Pose", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
