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
