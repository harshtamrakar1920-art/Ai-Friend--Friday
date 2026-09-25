import speech_recognition as sr
import webbrowser # can open browser to search anything
import pyttsx3 # text to speech
import musicLibrary
import requests
import os
from openai import OpenAI
from gtts import gTTS
import pygame




recognizer = sr.Recognizer() # a recognizer object , so it recognize whatever we speak , # sr.recognizer is a class which helps in taking s.r functionality
 # initializing pyttsx , # engine which initialize pyttsx
newsapi = "fb7f8eb9811e496bb22ec7a5d0a51ca3"





def speak_old(text): #  a speech fnc it will take a text and speak 
    engine  = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

# keep the program alive while it plays
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    

def aiprocess(command):
    client = OpenAI(
    api_key= os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
    )

    completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages =[
        {"role": "system","content" : "Your are a virtual assitant named friday skilled in genral tasks like Alexa and google cloud and give short responses"},
             {"role": "user", "content": command}  ]
)

    return completion.choices[0].message.content
  
def processCommand(c):
    if"open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com/")
    elif c.lower().startswith("play"):
         print("play is heard")
         song = c.lower().split(" ",1)[1]
         if song in musicLibrary.music:
          link = musicLibrary.music[song]
          webbrowser.open(link)
         else:
          speak(f"I don't have {song} in my library")
    elif "headlines" in c.lower():
       r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
       if r.status_code == 200:
          data = r.json()  # <-- fixed: added ()
          articles = data.get('articles', [])

          if not articles:
              speak("No news articles found")
          else:
               speak("Here are the top headlines")
               for article in articles[:5]:  # limit to top 5 so it doesn't ramble forever
                speak(article['title'])
    else:
        output = aiprocess(c)
        speak(output)
        # let open ai handle the request
    

if __name__ == "__main__":
    speak(" Initializing friday.......")

    with sr.Microphone() as source:
        print("Calibrating for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

    while True:
            # listen for the wake word "friday"
             # obtain audio from the microphone
        
        print("Listening....")
           # recognize speech using google
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout= 5, phrase_time_limit=3)
                
            print("recognizing...")
            word = recognizer.recognize_google(audio)
            print(f"Heard: {word}")

            if "friday" in word.lower():
                speak("Yes")
                
                    # Listen for command
                with sr.Microphone() as source:
                    print("friday active....")
                    audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                print(f"Command: {command}")

                processCommand(command)
        except Exception as e:
            print("google error; {0}".format(e))