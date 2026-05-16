import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def listen_voice():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return ""

def speak(text):
    engine.say(text)
    engine.runAndWait()