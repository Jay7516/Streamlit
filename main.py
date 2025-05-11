# import streamlit as st
# import random
# from utils.voice import generate_voice,terminate_voice
# from playsound import playsound
# from gemini_flash import generate_text
# st.write("## AI Response thing")
# question = st.text_input("Question")
# #FILE_PATH = "sound/Lego yoda death sound.mp3"
# FILE_PATH = "sound\Im Joe Biden and I approve this message.mp3"
# audio_value = st.audio_input("Record a voice message")
# if audio_value:
#     st.audio(audio_value)
# if 'response' not in st.session_state:
#     st.session_state.response = ""

# response = ""
# if st.button("Generate Response", key="button"):
#     response = generate_text(question)
#     generate_voice(response)
#     st.session_state.response = response
# st.text_area("Response", value=st.session_state.response)
     
# if st.button("Voice Terminate"):
#     terminate_voice()
# if st.button("Play Audio", key="play_audio_button"):
#    response = random.randint(0,3)
#    st.text_area("L",value=response)
#    #generate_voice("Hello there its nice to meet you")
#    playsound(FILE_PATH)
#    playsound(FILE_PATH)
#    playsound(FILE_PATH)
#    playsound(FILE_PATH)
#    #st.audio(FILE_PATH, format="audio/mpeg", loop=False,autoplay=True)