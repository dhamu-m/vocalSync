import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests

# Initialize speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 180)

# Speak out loud
def talk(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen to microphone
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.pause_threshold = 1
        audio = listener.listen(source, timeout=5, phrase_time_limit=10)
    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print(f"You: {command}")
        if "jarvis" in command:
            command = command.replace("jarvis", "").strip()
            return command
        else:
            return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        talk("Sorry, I am having trouble with the service.")
        return ""

# Respond to commands
def run_jarvis():
    command = take_command()
    if command == "":
        return

    # Time
    elif "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time}")

    # Wikipedia
    elif "who is" in command or "what is" in command:
        try:
            info = wikipedia.summary(command, sentences=2)
            talk(info)
        except:
            talk("Sorry, I couldn't find information on that.")

    # Play on YouTube
    elif "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    # Tell a joke
    elif "joke" in command:
        joke = pyjokes.get_joke()
        talk(joke)

    # Search on Google
    elif "search" in command:
        search_query = command.replace("search", "").strip()
        talk(f"Searching for {search_query}")
        pywhatkit.search(search_query)

    # Weather
    elif "weather" in command:
        talk("Please tell me the city name.")
        city = take_command()
        if city:
            api_key = "a4f675db4a38794dfb52618d2acf5f2c"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                response = requests.get(url).json()
                if response["cod"] != "404":
                    temp = response["main"]["temp"]
                    desc = response["weather"][0]["description"]
                    talk(f"The temperature in {city} is {temp} degrees Celsius with {desc}")
                else:
                    talk("City not found.")
            except:
                talk("Sorry, I couldn't connect to the weather service.")
        else:
            talk("City name not recognized.")

    # Exit
    elif "exit" in command or "stop" in command or "shutdown" in command:
        talk("Shutting down. Have a great day!")
        exit()

    # Fallback
    else:
        talk("I didn't understand that. Can you say it again?")

# Start assistant
talk("Hello! I am Jarvis, your AI voice assistant.")
talk("Say 'Jarvis' followed by your command.")

while True:
    run_jarvis()
