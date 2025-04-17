from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import traceback

# Setup Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="ExdTmiH9EHSp4DYnRxys"
)

# FastAPI app initialization
app = FastAPI()

# CORS setup
origins = [
    "http://localhost",  # Allow local frontend to communicate
    "http://localhost:3000",  # Adjust based on your frontend's URL if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Helper function for image inference
def infer_image(image: np.array):
    result = CLIENT.infer(image, model_id="final-missiles/2")

    for prediction in result['predictions']:
        x, y = int(prediction['x']), int(prediction['y'])
        w, h = int(prediction['width']), int(prediction['height'])
        x1, y1 = x - w // 2, y - h // 2
        x2, y2 = x + w // 2, y + h // 2
        label = prediction['class']

        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    return image


# FastAPI endpoint for image inference
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read image data from uploaded file
        image_data = await file.read()

        try:
            image = Image.open(BytesIO(image_data))
        except Exception as e:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        image = np.array(image)
        if image is None:
            raise ValueError("Invalid image data")

        # Perform inference
        result_image = infer_image(image)

        # Encode result image to send as response
        _, encoded_image = cv2.imencode('.jpeg', result_image)
        result_image_bytes = encoded_image.tobytes()

        # Return the image as a response
        return StreamingResponse(BytesIO(result_image_bytes), media_type="image/jpeg")

    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())  # Print stack trace for debugging
        raise HTTPException(status_code=400, detail=str(e))


# Running the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
