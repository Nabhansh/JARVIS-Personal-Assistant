import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 SAY SOMETHING…")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)
    print("Captured audio, trying to decode...")

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)