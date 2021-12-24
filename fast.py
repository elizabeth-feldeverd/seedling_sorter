from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
# from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from google.cloud import storage
import uuid

app = FastAPI()
# model = load_model("model.h5")
BUCKET = "sorting_bucket"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello Elizabeth!"}

@app.post("/sort")
def sort(file: UploadFile = File(...)):
    # Open the uploaded image
    image = Image.open(file.file)

    # Save the image as a png
    myuuid = uuid.uuid4()
    path = f"{myuuid}.png"
    image.save(path)

    # Upload png to Google Cloud Storage
    gcs = storage.Client()
    bucket = gcs.get_bucket(BUCKET)
    blob = bucket.blob(path)
    blob.upload_from_filename(path)

    return {
        "url": blob.public_url,
    }
