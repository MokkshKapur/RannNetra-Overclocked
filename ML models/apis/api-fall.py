from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
import base64
import os

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (you can restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ExdTmiH9EHSp4DYnRxys"
)

@app.post("/fall-detect/")
async def detect_fall(file: UploadFile = File(...)):
    # Read image bytes
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if image is None:
        return JSONResponse(content={"error": "Invalid image"}, status_code=400)

    # Save temp image
    temp_path = "temp.jpg"
    cv2.imwrite(temp_path, image)

    # Run inference
    result = CLIENT.infer(temp_path, model_id="fall_detection-8vxyk/2")

    # Draw predictions
    for prediction in result['predictions']:
        x = int(prediction['x'])
        y = int(prediction['y'])
        w = int(prediction['width'])
        h = int(prediction['height'])
        class_name = prediction['class']

        # Bounding box
        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        # Aspect ratio classification
        aspect_ratio = w / h
        if aspect_ratio > 1.3:
            fall_type = "Prone Position"
            color = (0, 0, 255)  # Red
        else:
            fall_type = "Normal Fall"
            color = (0, 255, 0)  # Green

        label = f"{class_name} - {fall_type}"
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Encode final image to base64
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Cleanup
    os.remove(temp_path)

    return {
        "predictions": result['predictions'],
        "image_base64": image_base64
    }

# Run server directly
if __name__ == "__main__":
    uvicorn.run("fall_api:app", host="0.0.0.0", port=8000, reload=True)
