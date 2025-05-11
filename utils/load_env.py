import os
from pathlib import Path

from dotenv import load_dotenv
gemini_key = ""
hf_key = ""
def load_env():
    global gemini_key
    global hf_key
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    envars = current_dir / ".env"
    print(envars)
    load_dotenv(envars)
    #print(os.getenv("GEMINI_KEY"),"DSGDSGDG")
    gemini_key = os.getenv("GEMINI_KEY")
    hf_key = os.getenv("HF_KEY")
    # Read environment variables
    #sender_email = os.getenv("EMAIL")
    #password_email = os.getenv("PASSWORD")
load_env()