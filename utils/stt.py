#from faster_whisper import WhisperModel
model_size = "large-v3"
# import whisper
# import os
import speech_recognition as sr
# Run on GPU with FP16
# model = WhisperModel(model_size, device="cpu", compute_type="float16")

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
    
    # model = whisper.load_model("turbo")
    # print(file_path.name)
    # # load audio and pad/trim it to fit 30 seconds
    # audio = whisper.load_audio(file_path.name)
    # audio = whisper.pad_or_trim(audio)

    # # make log-Mel spectrogram and move to the same device as the model
    # mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

    # # detect the spoken language
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")

    # # decode the audio
    # options = whisper.DecodingOptions()
    # result = whisper.decode(model, mel, options)
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    return text
if __name__ == "__main__":
    transcribe_audio()
#print("AI Response")
#print("\n" + generate_text(full_transcription + "summarize this text", "You are a wacky guy who summarize things weirdly",1.5).text)
