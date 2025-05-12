import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import json
from utils.sound_util import call_speak
import base64
from utils.stt import transcribe_audio
from utils.utils import markdown_to_text, get_path, clear_audio_folder
import sys
from utils.speakers import *
import tempfile
#sys.modules['torch.classes'].__path__ = []
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_KEY")

st.title("McDonald's Chatbot 🍔🤖🍟")
st.write("A chatbot that has the data about the Mcdonald's Canada menu. Whether you're curious about calories or checking ingredients this bot has all the answers—fast and friendly.")
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

    Based only on this data(don't mention that), please: Answer questions
    
    If the user ask to display an image, you MUST use Markdown format like this: ![alt text](URL)
    use the url from the json
    You must turn any Unicode encoding into its regular text
"""
default_prompt = "Answer questions in a respectful manner and don't overcomplicated your response."
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content=[response,default_prompt]
        )
    ]
if "audio_input" not in st.session_state:
    st.session_state.audio_input = None
    clear_audio_folder()


prompt = st.chat_input("Ask me anything about the McDonald's menu!")

def autoplay_audio(file_path: str, auto_play = True):
    autoplay_attr = "autoplay" if auto_play else ""
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls  {autoplay_attr}>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        return st.markdown(
            md,
            unsafe_allow_html=True,
        )
def remake_markdown(new_voice = False):
    
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
                if new_voice:
                    call_speak(markdown_to_text(message.content),speaker)
                    #autoplay_audio(get_path(),False)
                    st.audio(get_path())
                else:
                    #st.audio(message.additional_kwargs.get("speaker"))
                    autoplay_audio(message.additional_kwargs.get("speaker"),False)
speaker = st.sidebar.selectbox(
    "Select the speaker voice:",
    speakers,
    index = 33
)

if st.sidebar.button("Regenerate Voice"):
    clear_audio_folder()
    remake_markdown(True)
else:
    remake_markdown()
model = st.sidebar.radio(
    "Pick your model",
    ["Regular Model", "Schema aware model"],index=1)
if model == "Regular Model":
    st.session_state.messages[0].content[0] = "Answer Questions"
else:
    st.session_state.messages[0].content[0] = response
speak_voice = st.sidebar.checkbox("Speak on generation",value = True)
temp = st.sidebar.slider("Temperature", 0.0, 2.0, 0.5)
llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=temp
)
prompt_area = st.sidebar.text_area(label = "Give a prompt here", value=default_prompt,height=134)
st.session_state.messages[0].content[1] = prompt_area
audio = st.sidebar.audio_input("🎙️ Record your question here")


def create_message(message):
    with st.chat_message("user"):
        st.markdown(message)
        st.session_state.messages.append(HumanMessage(content=message))

    with st.chat_message("assistant"):
        output = llm.invoke(st.session_state.messages)
    
        st.markdown(output.content)

        call_speak(markdown_to_text(output.content),speaker)
        autoplay_audio(get_path(),speak_voice)
        st.session_state.messages.append(AIMessage(content=output.content,  additional_kwargs={"speaker": get_path()}))
if prompt:
    create_message(prompt)


if st.session_state.audio_input != audio:
    st.session_state.audio_input = audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio.getvalue())
        tmp_file_path = tmp_file.name
    create_message(transcribe_audio(tmp_file_path))
