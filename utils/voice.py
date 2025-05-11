import pyttsx3
from multiprocessing import Process

import edge_tts
import asyncio
from playsound import playsound
from time import sleep
import os
# Store current speech process in a global variable
current_process = None

# Function that actually does the speaking
def speak(content):
    engine = pyttsx3.init()
    engine.say(content)
    engine.runAndWait()

# Function to start speaking (terminates previous speech)
def generate_voice(content):
    global current_process
    # Terminate if already speaking
    terminate_voice()
    # Start new speech process
    current_process = Process(target=speak, args=(content,))
    current_process.start()

# Function to stop current speech
def terminate_voice():
    global current_process
    if current_process is not None and current_process.is_alive():
        current_process.terminate()
        current_process.join()
        current_process = None

async def speak_chinese(text, voice="zh-HK-HiuGaaiNeural"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")


def call_speak(text):
    asyncio.run(speak_chinese(text))
    # loop = asyncio.get_event_loop()
    # if loop.is_running():
    #     # We're already inside an event loop (e.g., in Jupyter or an async app)
    #     asyncio.create_task(speak_chinese(text))
    # else:
    #     loop.run_until_complete(speak_chinese(text))

# # Example usage
# call_speak("我喜欢学习中文")