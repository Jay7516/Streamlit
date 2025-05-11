import edge_tts
import asyncio
from playsound import playsound
import os
import pyttsx3
from multiprocessing import Process

FILEPATH = "sound\Im Joe Biden and I approve this message.mp3"


def play_sound():
    playsound(FILEPATH)


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


async def speak_voice(text, voice="zh-HK-HiuGaaiNeural"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")

def call_speak(text):
    asyncio.run(speak_voice(text, voice="en-US-AvaNeural"))