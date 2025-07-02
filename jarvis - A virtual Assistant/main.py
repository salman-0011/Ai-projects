import speech_recognition as sr
import webbrowser
from gtts import gTTS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')


# models = genai.list_models()

# for model in models:
#     print(f"Model: {model.name}, Supported Methods: {model.supported_generation_methods}")
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("mpg123 temp.mp3")
    os.remove("temp.mp3")
def processCommand(c):
    if("open google" in c.lower()):
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif("open youtube" in c.lower()):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif("open linkedin" in c.lower()):
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com")
    elif("your name" in c.lower()):
        speak("I am Jarvis, your personal assistant.")
    elif("tell me a joke" in c.lower()):
        speak("Why did the computer go to the doctor? Because it had a virus!")
    else:
        # If no known command, fallback to Gemini
        try:
            response = model.generate_content(c)
            reply = response.text.strip()
            speak(reply)
        except Exception as e:
            print("Gemini error:", e)
            speak("Sorry, I couldn't process that.")
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)
                print("recogninzing....")
                print(word)
                if(word.lower() == "jarvis"):
                    speak("Sir, How can i help you")
                    with sr.Microphone() as source:
                        print("jarvis is active")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
            except Exception as e:
                print(f"Error: {e}")
