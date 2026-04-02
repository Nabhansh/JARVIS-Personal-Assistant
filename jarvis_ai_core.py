import os
import threading
import time
import webbrowser
import subprocess

import psutil
import speech_recognition as sr

import pyttsx3

# =============== CONFIG ===============
OPENAI_API_KEY = ""   # optional for now
# =====================================

# ---------- TTS ----------
# engine = pyttsx3.init()
# engine.setProperty("rate", 175)
# engine.setProperty("volume", 1.0)

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)

    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    del(engine)
    # print('I have run and am waiting')

# ---------- STT ----------
listener: sr.Recognizer = sr.Recognizer()
listener.energy_threshold = 300
listener.dynamic_energy_threshold = True
listener.pause_threshold = 0.8

mic = sr.Microphone()

# Calibrate ONCE (IMPORTANT)
with mic as source:
    print("🎤 Calibrating microphone...")
    listener.adjust_for_ambient_noise(source, duration=1)
    print("🎤 Mic calibration done.")

def set_state(state, cmd=""):
    os.system(f"title JARVIS - State: {state} {cmd}")
    print(f"[STATE] {state} {cmd}")

def listen_once(timeout=6, phrase_time_limit=8):
    with mic as source:
        try:
            print("Listening...")
            audio = listener.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
        except Exception as e:
            print("Listen error:", e)
            return None

    try:
        text = listener.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("STT error:", e)
    return None

# ---------- SYSTEM COMMANDS ----------
def open_application(cmd):
    if "chrome" in cmd:
        speak("Opening Chrome")
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
    elif "code" in cmd:
        speak("Opening Visual Studio Code")
        subprocess.Popen(
            r"C:\Users\Rishi Gaur\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        )
    else:
        speak("I don't know that application yet")

def system_status():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    speak(f"CPU {cpu} percent, memory {mem} percent")

def handle_command(cmd):
    if not cmd:
        return

    if "open" in cmd:
        open_application(cmd)
    elif "status" in cmd or "cpu" in cmd:
        system_status()
    elif "search" in cmd or "google" in cmd:
        q = cmd.replace("search", "").replace("google", "")
        speak(f"Searching {q}")
        webbrowser.open(f"https://google.com/search?q={q}")
    else:
        speak("Command received, but AI brain not connected yet.")

# ---------- MAIN LOOP ----------
def jarvis_loop():
    speak("JARVIS online. Say Hey Jarvis.")

    while True:
        set_state("IDLE")

        text = listen_once()
        if not text:
            continue

        if "jarvis" in text:
            set_state("LISTENING")
            speak("Yes sir. How can I help you?")

            cmd = listen_once()
            if not cmd:
                set_state("IDLE")
                continue

            set_state("EXECUTING", cmd)
            handle_command(cmd)
            set_state("IDLE")

def start_jarvis_background():
    t = threading.Thread(target=jarvis_loop, daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    jarvis_loop()