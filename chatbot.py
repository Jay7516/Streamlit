import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import json
from utils.sound_util import call_speak,generate_voice
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

    Based only on this data, please: Answer questions in a respecful manner without any bold text or -
"""
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content=response
        )
    ]

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

prompt = st.chat_input("Ask me anything about the mcdonald menu!")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)

        st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):

        output = llm.invoke(st.session_state.messages)
    
        st.markdown(output.content)
        st.session_state.messages.append(AIMessage(content=output.content))
        generate_voice(output.content)