import streamlit as st
import pathlib
import numpy as np
from PIL import Image
from skimage import transform
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications import mobilenet_v2

st.set_page_config(page_title="Seedling Sorter", page_icon="🌱")

STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
)  # at venv/lib/python3.9/site-packages/streamlit/static

st.markdown("""
    # Seedling Sorter
""")

png = st.file_uploader("Upload an image of a seedling",
                       type=([".png"]))

def load_img(png):
    # Preprocesses the png prior to making predictions
    np_image = Image.open(png)
    np_image = img_to_array(np_image)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (256, 256, 3))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image

def predict(img):
    # Predicts the species of the plant in img
    model = load_model("model.h5")
    predictions = model.predict(img)
    return predictions

def process_predict(predictions):
    labels = [
        'Black-grass', 'Charlock', 'Cleavers', 'Common Chickweed',
        'Common wheat', 'Fat Hen', 'Loose Silky-bent', 'Maize',
        'Scentless Mayweed', 'Shepherds Purse', 'Small-flowered Cranesbill',
        'Sugar beet'
    ]
    MaxPosition=np.argmax(predictions)
    prediction_label=labels[MaxPosition]
    return prediction_label

if png:
    img = load_img(png)
    result = predict(img)
    # st.write(result)
    predicted_labels = process_predict(result)
    st.write(predicted_labels)
    # st.write(result.argmax(axis=-1))
