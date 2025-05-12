import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import json
from utils.sound_util import call_speak,generate_voice
import base64
from utils.stt import transcribe_audio
from utils.utils import markdown_to_text
import sys
#sys.modules['torch.classes'].__path__ = []
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_KEY")
llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0.5
)

st.title("🍟🍔 Mcdonald Chatbot")
json_string_for_prompt = ""
with open("json/data/mc_data.json", 'r') as f:
    # Load JSON data into a Python dictionary/list
    data_dict = json.load(f)
    # Convert the Python dictionary/list back to a formatted JSON string
    # This is good for including in the prompt so Gemini sees it as JSON
    json_string_for_prompt = json.dumps(data_dict, indent=2)
response = f"""
    Here is some data in JSON format:
    ```json
    {json_string_for_prompt}
    ```

    Based only on this data(don't mention that), please: Answer questions in a respecful manner and don't overcomplicated info
    
    If the user ask to display an image, you MUST use Markdown format like this: ![alt text](URL)
    use the url from the json
"""
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content=response
        )
    ]
# if "audio_processed" not in st.session_state:
#     st.session_state.audio_processed = None

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
spacer = st.empty()

prompt = st.chat_input("Ask me anything about the McDonald's menu!")

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
st.divider()  # Optional visual separation
# Simulated audio-to-text transcription (placeholder)
def create_message(message):
    with st.chat_message("user"):
        st.markdown(message)

        st.session_state.messages.append(HumanMessage(content=message))

    with st.chat_message("assistant"):
        output = llm.invoke(st.session_state.messages)
    
        st.markdown(output.content)
        st.session_state.messages.append(AIMessage(content=output.content))
        call_speak(markdown_to_text(output.content))
        autoplay_audio("output.mp3")
chat_input = False
if prompt:
    create_message(prompt)
    chat_input = True
audio = st.audio_input("🎙️ Or record your question")
import tempfile
if audio and not chat_input:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio.getvalue())
        tmp_file_path = tmp_file.name
    create_message(transcribe_audio(tmp_file_path))