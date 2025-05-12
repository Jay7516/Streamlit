#from faster_whisper import WhisperModel
model_size = "large-v3"
from openai import OpenAI
# Run on GPU with FP16
#model = WhisperModel(model_size, device="cpu", compute_type="float16")

# def transcribe_audio(file_path):
#     segments, info = model.transcribe(file_path, beam_size=7)
#     print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
#     full_transcription = ""
#     #full_transcription = " ".join(segment.text for segment in segments)
#     for segment in segments:
#         #print(segment.text)
#         full_transcription += segment.text + " "
#     #os.remove(file_path)
#     return full_transcription
def transcribe_audio(file_path):
    client = OpenAI()
    audio_file= open("/path/to/file/audio.mp3", "rb")

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-transcribe", 
        file=audio_file,
        response_format="text"
    )
    return transcription.text
if __name__ == "__main__":
    transcribe_audio()
#print("AI Response")
#print("\n" + generate_text(full_transcription + "summarize this text", "You are a wacky guy who summarize things weirdly",1.5).text)
