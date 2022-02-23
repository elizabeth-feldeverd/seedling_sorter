import pathlib
from os.path import join, isfile, dirname
from os import listdir
from itertools import cycle
import streamlit as st
import numpy as np
from PIL import Image
from skimage import transform
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

st.set_page_config(page_title="Seedling Sorter", page_icon="🌱")

STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
)

# Header and body text
st.title("Seedling Sorter")
st.subheader(
    "Deep learning app that predicts the\
    species of a young plant with 81% accuracy."
)
st.write(
    "My objective was to create a tool that could quickly and\
    accurately classify seedlings (young plants).\
    One possible application of this model is **precision weed management**,\
    where weeds are identified and removed in real time using sensors,\
    a tractor, weeding tools, and a computer to process images with the model.\
    Such technology can reduce manual labor and herbicide use."
)
st.write(
    "If you'd like to learn more, connect with me, Elizabeth Oda, via\
    [GitHub](https://github.com/elizabeth-oda) or\
    [LinkedIn.](https://www.linkedin.com/in/elizabethoda/)"
)

# Returns the file names for example images
file_dir = join(dirname(__file__), "test_img")
file_names = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]

# Creates a list with example images
img_list = []
for img in file_names:
    img_path = join(file_dir, img)
    to_image = Image.open(img_path)
    img_list.append(to_image)

# Displays and captions example images
st.subheader("Representative images of the 12 species in the dataset")
st.write(
    "You can **drag and drop any of the images below**, or upload your own.\
    This model only works seedlings of the twelve species shown below.\
    Please note that the images shown here were not used to train the model."
)
cols = cycle(st.columns(3))
for label, img in enumerate(img_list):
    next(cols).image(img, width=180, caption=file_names[label].replace('.png', ''))

def load_img(png):
    # Preprocesses the png prior to making predictions
    np_image = Image.open(png)
    np_image = img_to_array(np_image)
    np_image = transform.resize(np_image, (128, 128, 3))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image

def predict(img):
    # Predicts the species of the plant in img
    model = load_model("model.h5")
    result = model.predict(img)
    return result

def process_predict(result):
    # Assigns a label to the top prediction
    # Keras models return predictions in alphabetical order of original labels
    labels = [
        'Black-grass', 'Charlock', 'Cleavers', 'Common Chickweed',
        'Common wheat', 'Fat Hen', 'Loose Silky-bent', 'Maize',
        'Scentless Mayweed', 'Shepherds Purse', 'Small-flowered Cranesbill',
        'Sugar beet'
    ]
    # Creates a dictionary matching predictions with species
    predictions = dict(zip(labels, result[0]))
    return predictions

# Allows users to upload and image
st.header("Try it out!")
png = st.file_uploader("Upload an image of a seedling")

# The model makes predictions and displays them
if png:
    img = load_img(png)
    result = predict(img)
    predictions = process_predict(result)
    top_three = dict(sorted(predictions.items(), key=lambda x: -x[1])[:3])
    st.header("Your Results")
    for l, p in top_three.items():
        st.subheader(l)
        st.write("Probability: " + str(round(p*100, 1)) + "%")
