import pyttsx3  # converts text to speech
import datetime  # required to resolve any query regarding date and time
import speech_recognition as sr  # required to return a string output by taking microphone input from the user
import wikipedia  # required to resolve any query regarding wikipedia
import webbrowser  # required to open the prompted application in web browser
import os.path  # required to fetch the contents from the specified folder/directory
import smtplib  # required to work with queries regarding e-mail
import re
from pyowm import OWM
from bs4 import BeautifulSoup as soup
import json
from time import strftime
import urllib
import sys
from newsapi import NewsApiClient
import bs4 as bs
import urllib.request
import requests
from gtts import gTTS
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')  # gets you the details of the current voices
engine.setProperty('voice', voices[1].id)  # 0-male voice , 1-female voice


def speak(audio):  # function for assistant to speak
    engine.say(audio)
    engine.runAndWait()  # to make assistant audible to user


def record_audio(ask=""):
    r = sr.Recognizer()
    with sr.Microphone() as source:  # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source, 5, 5)  # listen for the audio via source
        print("Done Listening")
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')  # error: recognizer is not connected
        print(">>", voice_data.lower())  # print what user said
        return voice_data.lower()


def wishme():  # function to wish the user according to the daytime
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning')

    elif hour > 12 and hour < 18:
        speak('Good Afternoon')

    else:
        speak('Good Evening')

    speak('Hello there!! I am Capable, your Artificial intelligence assistant. May I know your name please?')


def news():
    newsapi = NewsApiClient(api_key='bd3740a807db4d1985dac2bee9b00817')
    speak("What topic would you like to hear the news about?")
    topic = takecommand()
    data = newsapi.get_top_headlines(q=topic, language="en", page_size=5)
    newsData = data["articles"]
    for y in newsData:
        speak(y["description"])


def weather():
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q=Doha&appid=0b32a4003866116b05179ea703dd2cb0&units=metric").json()
    temp1 = res["weather"][0]["description"]
    temp2 = res["main"]["temp"]
    speak(f"Temperature is {format(temp2)} degree Celsius \nWeather is {format(temp1)}")


def takecommand():  # function to take an audio input from the user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 2
        audio = r.listen(source)

    try:  # error handling
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')  # using google for voice recognition
        print(f'User said: {query}\n')

    except Exception as e:
        print('Say that again please...')  # 'say that again' will be printed in case of improper voice
        speak('I did not understand. Say that again please')
        return 'None'
    return query


def exists(terms):
    for term in terms:
        if term in query:
            return True


def sendemail(to, content):  # function to send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()


if __name__ == '__main__':
    wishme()
    while True:
        query = takecommand().lower()  # convert user query into lower case

        if exists(["my name is", "name is"]):
            person_name = query.split("is")[-1].strip()
            speak("Nice to meet you" + person_name)
            speak("Please tell me how may I help you")

        # search up stuff on wikipedia

        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=5)
            print(results)
            speak(results)

        # search on google

        elif exists(["search for"]) and 'youtube' not in query:
            search_term = query.split("for")[-1]
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            speak("Here is what I found for" + search_term + "on google")

        elif exists(["search"]) and 'youtube' not in query:
            search_term = query.replace("search", "")
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            speak("Here is what I found for" + search_term + "on google")

        # search on youtube

        elif exists(["youtube"]):
            search_term = query.split("for")[-1]
            search_term = search_term.replace("on youtube", "").replace("search", "")
            url = "https://www.youtube.com/results?search_query=" + search_term
            webbrowser.get().open(url)
            speak("Here is what I found for " + search_term + "on youtube")

        # tell the user's current location

        elif exists(["where am I", "what is my location", "what is my current location", "tell me my location"]):
            url = "https://www.google.com/maps/search/Where+am+I+?/"
            webbrowser.get().open(url)
            speak("You must be somewhere near here, as per Google maps")

            # tell the user the current time

        elif exists(["what's the time", "tell me the time", "what time is it", "what is the time"]):
            strtime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'The time right now is {strtime}')

        # miscellaneous websites
        elif exists(["open stack overflow", "stack overflow", "stackoverflow"]):
            webbrowser.open('stackoverflow.com')


        elif exists(["open free code camp", "open code camp", "code camp"]):
            webbrowser.open('freecodecamp.org')

        # open social media

        elif 'open twitter' in query:
            speak("Here you go to Twitter")
            webbrowser.open("twitter.com")


        elif 'open instagram' in query:
            speak("Here you go to Instagram")
            webbrowser.open("instagram.com")


        elif 'open facebook' in query:
            speak("Here you go to Facebook")
            webbrowser.open("facebook.com")

        # make small talk with the user

        elif exists(["how are you", "how are you doing"]):
            speak("I am fine, Thank you. I hope you're doing well too!")


        elif exists(["I am fine thankyou", "I am doing good", "I am fine", "okay"]):
            speak("It's good to know that your fine")


        elif exists(["what's your name", "do you have a name"]):
            speak("My friends call me Capable. what is your name?")


        elif exists(["who made you", "who created you", "who's your developer"]):
            speak(
                "I have been created by a group of really nice people. Feel free to check out the ABOUT tab for more info.")

        elif exists(["what's your favourite color", "do you like any color", "color", "what is your favorite color"]):
            speak("I really like : the colour of clouds  :   but it is  a bit complex to explain.")

        elif exists(["who are you", "what are you"]):
            speak("I am Capable. Your desktop assistant.")

        elif 'email' in query:
            try:
                speak('what should i write in the email?')
                content = takecommand()
                to = 'receivers_email@gmail.com'
                sendemail(to, content)
                speak('email has been sent')
            except Exception as e:
                print(e)
                speak('Sorry, I am not able to send this email')

        # tell the current news

        elif exists(["current news", "latest news", "news", "news update"]):
            news()

        # tell the weather

        elif exists(["what's the weather", "temperature", "weather forecast for today", "today's forecast", "weather"]):
            weather()

        # open reddit

        elif exists(["open reddit", "reddit"]):
            reg_ex = re.search('open reddit (.*)', query)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            speak('The Reddit content has been opened for you.')

        # greet the user

        elif 'hello' in query:
            day_time = int(strftime('%H'))
            if day_time < 12:
                speak('Good morning')
            elif 12 <= day_time < 18:
                speak('Good afternoon')
            else:
                speak('Good evening')

        # tell jokes/pun

        elif exists(["tell me a joke", "jokes", "do you have any jokes?", "tell me a pun", "pun"]):
            jokes = ["How do celebrities stay cool? ; They have many fans",
                     " What do you call it when Batman skips church? ; Christian Bale",
                     " Why are skeletons so calm? ; Because nothing gets under their skin",
                     " Don't trust atoms. ; They make up everything!",
                     "Never buy anything with velcro. ; It's a total rip-off.",
                     "I would tell you a joke about pizza ; but it's a little cheesy.",
                     "Why did the man fall down the well? ; Because he couldn’t see that well.",
                     "What does a lemon say when it answers the phone? ; Yellow!"]
            pun = random.choice(jokes)
            speak(pun)

        # play games with user

        elif exists(["game", "Lets play a game", "i want to play a game", "play a game"]):
            voice_data = record_audio("choose from rock, paper or scissor")
            moves = ["rock", "paper", "scissor"]

            cmove = random.choice(moves)
            pmove = voice_data

            speak("The computer chose " + cmove)
            speak("You chose " + pmove)

            if pmove == cmove:
                speak("the match is draw")
            elif pmove == "rock" and cmove == "scissor":
                speak("Player wins")
            elif pmove == "rock" and cmove == "paper":
                speak("Computer wins")
            elif pmove == "paper" and cmove == "rock":
                speak("Player wins")
            elif pmove == "paper" and cmove == "scissor":
                speak("Computer wins")
            elif pmove == "scissor" and cmove == "paper":
                engine_speak("Player wins")
            elif pmove == "scissor" and cmove == "rock":
                speak("Computer wins")

        elif exists(["toss", "flip", "coin", "toss a coin", "flip a coin", "coin toss"]):
            moves = ["head", "tails"]
            cmove = random.choice(moves)
            speak("The computer chose " + cmove)

        # list out the functions the assistant can perform

        elif exists(["what functions can you perform", "menu", "list of commands", "list of functions",
                     "what all functions can you perform", "what can you do?"]):
            speak("""
            You can use these commands : and I'll help you out:
            Number 1: Open : reddit : subreddit : Opens the subreddit in default browser.
            Number 2: top stories : from current news
            Number 3: Send email : Follow up questions such as recipient name, content will be asked in order.
            Number 4: Current weather in {cityname} : Tells you the current weather condition : and temperature of your location
            Number 5: Greet the user
            Number 6: Open any website :  play the indicated video from youtube : and open social media
            Number 7: Interact with the user
            Number 8: Tell you your current location
            Number 9: time : tells the current time : according to your location
            Number 10: Shut down the application upon request
            Feel free to check out the MENU tab for more info
        """)


        # close the application

        elif exists(["close", "shut down", "power off", "Bye", "Thats all for now", "Good bye", "exit", "quit"]):
            speak('Sure! please call me when you need me. Have a nice day')
            sys.exit()








