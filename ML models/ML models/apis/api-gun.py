from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
import os
import base64

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins (adjust for production)
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

@app.post("/detect/")
async def detect_threat(file: UploadFile = File(...)):
    # Read image
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if image is None:
        return JSONResponse(content={"error": "Invalid image"}, status_code=400)

    # Save temp image
    temp_path = "temp.jpg"
    cv2.imwrite(temp_path, image)

    # Inference
    result = CLIENT.infer(temp_path, model_id="threat-detection-xoido/1")

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

    # Convert annotated image to base64
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Remove temp file
    os.remove(temp_path)

    return {
        "predictions": result['predictions'],
        "image_base64": image_base64
    }

# Run the app if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
