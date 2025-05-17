from markdown import markdown
from bs4 import BeautifulSoup
import os
def markdown_to_text(md):
    # Convert markdown to HTML
    html = markdown(md)
    # Strip HTML tags
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


unqiue_path = None
def get_unique_filepath(base_name="output", ext="mp3", folder="audio"):
    global unqiue_path
    counter = 1
    while True:
        file_path = os.path.join(folder, f"{base_name}_{counter}.{ext}")
        if not os.path.exists(file_path):
            unqiue_path = file_path
            return file_path
        counter += 1
def get_path():
    return unqiue_path

def clear_audio_folder(folder="audio"):
    if not os.path.exists(folder):
        return  # nothing to clear if folder doesn't exist

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):  # ensure it's a file
            os.remove(file_path)

from PIL import Image
import numpy as np
import requests
from io import BytesIO

def darken_white_background(url, threshold=240, darkness=160):
    # Load image from URL
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    img = Image.open(BytesIO(response.content)).convert("RGB")

    # Convert to NumPy array
    data = np.array(img)
    
    # Create a mask for white-ish pixels
    white_mask = np.all(data >= threshold, axis=-1)
    
    # Define darker background color (e.g., dark gray)
    dark_bg_color = [darkness, darkness, darkness]

    # Apply the dark color to white areas
    data[white_mask] = dark_bg_color

    # Convert back to image
    result_img = Image.fromarray(data)

    return result_img
# Example usage
url = "https://s7d1.scene7.com/is/image/mcdonalds/mcdonalds-cheeseburger-happy-meal-apples-1:product-header-mobile?wid=768&hei=441&dpr=off"
dark_img = darken_white_background(url)
dark_img.show() 