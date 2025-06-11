import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from ultralytics import YOLO
from io import BytesIO
import uvicorn

# Load YOLO-OBB model
model = YOLO("runs/obb/train6/weights/best.pt")  # Make sure this is a valid path to your model

app = FastAPI()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read image into OpenCV format
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run YOLO-OBB prediction
    results = model.predict(source=img, imgsz=1024, conf=0.25)

    # Draw oriented bounding boxes (OBB)
    for r in results:
        for box in r.obb.xyxyxyxy:
            box = box.cpu().numpy().astype(int)
            pts = box.reshape(-1, 1, 2)
            cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    # Encode image to JPEG and return as response
    _, img_encoded = cv2.imencode(".jpg", img)
    return StreamingResponse(BytesIO(img_encoded.tobytes()), media_type="image/jpeg")

# For running directly with Python
if __name__ == "__main__":
    uvicorn.run("dota 8 api:app", host="0.0.0.0", port=8000, reload=True)
