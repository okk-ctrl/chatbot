import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text 
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]

# if "audio_initialized" not in st.session_state:
st.session_state.audio_initialized = False

initialize_session_state()

st.title("OpenAI Conversational Chatbot ")

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes =  audio_recorder

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    #WRITE THE AUDIO BYTES TO A FILE
    with st.spinner("Transcribing...."):
        audio_file = "temp_audio.mp3"
        with open(audio_file,"wb") as f:
            f.write(audio_bytes)

            transcript =  speech_to_text(audio_file)
            if transcript:
                st.session_state.messages.append({"role": "user", "content":
                transcript})
                with st.chat_message("user"):
                    st.write(transcript)
                os.remove(audio_file)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking.........."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response...."):
            audio_file2 = text_to_speech( final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file2)

footer_container.float("bottom: 0rem;")
