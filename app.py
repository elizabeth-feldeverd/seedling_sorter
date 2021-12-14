import streamlit as st
from PIL import Image
import requests
import pathlib
import uuid

st.set_page_config(page_title="Seedling Sorter", page_icon="🌱")

STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
)  # at venv/lib/python3.9/site-packages/streamlit/static

st.markdown("""
    # Seedling Sorter
""")

png = st.file_uploader("Upload an image of a seedling",
                       type=([".png"]))

if png:
    # save png
    myuuid = uuid.uuid4()
    IMG1 = f"{myuuid}.png"

    url = "http://127.0.0.1:8000/annotate"  # local
    # url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": (png.name, png, "multipart/form-data")}
    response = requests.post(url, files=files).json()

    # How to download image from url
    IMG2 = response["url"]

    original = Image.open(png)
    width, height = original.size
    height = 705 / width * height
    original.save(STREAMLIT_STATIC_PATH / IMG1)  # this overwites
