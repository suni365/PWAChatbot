import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import speech_recognition as sr
import numpy as np
import queue

st.title("Live Voice Chatbot 🎙️")

# Queue to store audio frames
audio_queue = queue.Queue()

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def recv(self, frame):
        audio_array = frame.to_ndarray()
        audio_queue.put(audio_array)
        return frame

def transcribe_audio():
    if not audio_queue.empty():
        audio_data = audio_queue.get()
        try:
            # Convert audio data to text
            with sr.AudioData(audio_data, 16000, 2) as source:
                text = sr.Recognizer().recognize_google(source)
                return text
        except sr.UnknownValueError:
            return "Could not understand audio"
    return ""

# WebRTC Microphone Input
webrtc_streamer(key="speech",
                mode=WebRtcMode.SENDRECV,
                audio_processor_factory=AudioProcessor,
                media_stream_constraints={"video": False, "audio": True})

st.write("Listening... Speak into the microphone.")

# Show Transcription in real-time
if st.button("Transcribe"):
    transcript = transcribe_audio()
    st.write(f"🗣️ **You Said:** {transcript}")