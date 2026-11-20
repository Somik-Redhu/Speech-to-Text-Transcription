import streamlit as st
import speech_recognition as sr
import io

st.set_page_config(page_title="Speech-to-Text", page_icon="🎙️")

st.title("🎙️ Speech-to-Text Transcription")
st.write("Upload an audio recording and convert its speech into text.")

audio_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "aiff", "aif", "flac"]
)

if audio_file is not None:
    st.audio(audio_file)

    if st.button("Transcribe Audio"):
        recognizer = sr.Recognizer()

        try:
            audio_bytes = audio_file.getvalue()

            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                st.info("Reading audio...")
                audio_data = recognizer.record(source)

            with st.spinner("Converting speech to text..."):
                transcript = recognizer.recognize_google(
                    audio_data,
                    language="en-US"
                )

            st.success("Transcription completed!")
            st.subheader("Your Transcript")
            st.text_area("Converted text", transcript, height=200)

            st.download_button(
                label="Download Transcript",
                data=transcript,
                file_name="transcription.txt",
                mime="text/plain"
            )

        except sr.UnknownValueError:
            st.error("Sorry, the speech could not be understood. Try a clearer recording.")
        except sr.RequestError as error:
            st.error(f"Speech recognition service error: {error}")
        except Exception as error:
            st.error(f"Something went wrong: {error}")
