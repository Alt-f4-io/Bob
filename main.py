from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import datetime
import os
import subprocess
import wolframalpha
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app_id = os.getenv('WOLFRAMALPHA_CLIENT_ID')

os.environ['WOLFRAMALPHA_CLIENT_ID'] = 'username'



recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Go Shopping', 'Clean Room']

def date():
    cleared == False
    date = datetime.datetime.today().strftime("%A the %d of %B %Y")
    speaker.say(date)
    speaker.runAndWait()

def time():
    cleared == False
    time = datetime.datetime.now().strftime("The time is %#I %M %p")
    speaker.say(time)
    speaker.runAndWait()

def open_youtube():
    cleared == False
    os.system('cmd /c start chrome "youtube.com"')

def create_note():
    global recognizer

    cleared == False

    speaker.say("What is your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
                filename = filename + ".txt"

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()
            subprocess.call(['notepad.exe', filename])

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again")


def add_todo():

    global recognizer
    cleared == False
    speaker.say("What do you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                f = open('todo.txt', 'a')
                f.write(item)
                f.write("\n")
                f.close()

                done = True

                speaker.say(f"I added {item} to the to do list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand. Please try again")
            speaker.runAndWait()


def show_todos():
    cleared == False
    speaker.say("The items on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    cleared == False
    speaker.say("Hello I am bob what can I do for you")
    speaker.runAndWait()


def quit():
    cleared == False
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)

def restart():
    cleared == False
    subprocess.call(["shutdown", "/r"])

def shutdown():
    cleared == False
    subprocess.call(["shutdown", "/s"])

def question():
    cleared == False
    speaker.say("What is your question?")
    speaker.runAndWait()

    global recognizer
    global app_id

    done = False

    while not done:
        try:
           with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                question = recognizer.recognize_google(audio)
                question = question.lower()

                client = wolframalpha.Client(app_id)

                question_understood = False
                
                while not question_understood:

                    try:
                        res = client.query(question)

                        answer = next(res.results).text

                        speaker.say(answer)
                        speaker.runAndWait()

                        done = True

                        question_understood = True
                    except:
                        speaker.say("Question was not understood.")

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand. Please try again")
            speaker.runAndWait()

mappings = {
    "greeting": hello,
    "create_note": create_note,
    #"add_todo": add_todo,
    #"show_todo": show_todos,
    "exit": quit,
    "date": date,
    "time": time,
    "open_youtube": open_youtube,
    "question": question,
    "restart": restart,
    "shutdown": shutdown
}

speaker.say("loading")
speaker.runAndWait()
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.load_model()
speaker.say("Ready")
speaker.runAndWait()
while True:
    cleared = False
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()
    except speech_recognition.UnknownValueError:
        message = ''
    if 'bob' in message:
        print("accepted")
        speaker.say("Yes?")
        speaker.runAndWait()
        cleared = True
        while cleared:
            try:
                with speech_recognition.Microphone() as mic:

                    recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = recognizer.listen(mic)

                    message = recognizer.recognize_google(audio)
                    message = message.lower()

                assistant.request(message)
                print("success")
                cleared == False
            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
                speaker.say("I could not hear you try again")
                speaker.runAndWait()
                print("unsuccessfull")

    
