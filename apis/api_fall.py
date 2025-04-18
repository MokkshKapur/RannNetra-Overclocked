from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
import shutil
import uvicorn
import os
from io import BytesIO

app = FastAPI()

# Enable CORS for all origins (customize for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Roboflow client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ExdTmiH9EHSp4DYnRxys"
)

@app.post("/detect-fall/")
async def detect_fall(file: UploadFile = File(...)):
    # Save uploaded image
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read image
    image = cv2.imread(temp_path)

    # Run inference
    result = CLIENT.infer(temp_path, model_id="fall_detection-8vxyk/2")

    # Clean up temp file
    os.remove(temp_path)

    # Annotate image
    for prediction in result['predictions']:
        x = int(prediction['x'])
        y = int(prediction['y'])
        w = int(prediction['width'])
        h = int(prediction['height'])
        class_name = prediction['class']

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

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

    # Encode image to return
    _, img_encoded = cv2.imencode(".jpg", image)
    img_bytes = BytesIO(img_encoded.tobytes())

    return StreamingResponse(img_bytes, media_type="image/jpeg")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_fall:app", host="0.0.0.0", port=8005, reload=True)

