from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from inference_sdk import InferenceHTTPClient
import cv2
import shutil
import os
from io import BytesIO

app = FastAPI()

# Enable CORS for all origins (customize if needed)
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

@app.post("/detect-gun/")
async def detect_gun(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read image using OpenCV
    image = cv2.imread(temp_path)
    if image is None:
        os.remove(temp_path)
        return {"error": "Unable to read image."}

    # Inference
    result = CLIENT.infer(temp_path, model_id="threat-detection-xoido/1")
    os.remove(temp_path)

    # Draw predictions
    for pred in result['predictions']:
        x, y = int(pred['x']), int(pred['y'])
        w, h = int(pred['width']), int(pred['height'])
        class_name = pred['class']

        x1, y1 = x - w // 2, y - h // 2
        x2, y2 = x + w // 2, y + h // 2

        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, class_name, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Convert image to JPEG
    _, img_encoded = cv2.imencode(".jpg", image)
    img_bytes = BytesIO(img_encoded.tobytes())

    return StreamingResponse(img_bytes, media_type="image/jpeg")

# Run app directly (when you use `python api_gun.py`)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_gun:app", host="0.0.0.0", port=8006, reload=True)
