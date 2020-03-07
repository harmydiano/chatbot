import flask
from flask import request, jsonify
import aiml
import os

import time, sys
import warnings
from raven import *
from weather import showrealtimeWeatherinfo, queryrealtimeWeatherinfo

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

mode = "text"
terminate = []
br = ['bag', 'sandal', 'car', 'house']

kernel = aiml.Kernel()

kernel.setBotPredicate("name", "Nyra")
kernel.setBotPredicate("city", "Nwogu")
kernel.setBotPredicate("email", "nyra@karixchange.com")
kernel.setBotPredicate("phylum", "computer program")
kernel.setBotPredicate("species", "robot")
kernel.setBotPredicate("nationality", "Nwogu, a land far within the clouds ")
kernel.setBotPredicate("location", "Nwogu, a land far within the clouds ")
kernel.setBotPredicate("language", "python")
kernel.setBotPredicate("favortemovie", "Avengers Infinity War")
kernel.setBotPredicate("kindmusic", "Coldplay")
kernel.setBotPredicate("domain", "Robot")
kernel.setBotPredicate("gender", "androgynous")
kernel.setBotPredicate("birthday", "2018")
kernel.setBotPredicate("botmaster", "KariXchange")
kernel.setBotPredicate("master", "KariXchange")
kernel.setBotPredicate("genus", "robot")
kernel.setBotPredicate("size", " 1 TB")
kernel.setBotPredicate("order", "artificial intelligence")
kernel.setBotPredicate("party", "none")
kernel.setBotPredicate("birthplace", "Earth")
kernel.setBotPredicate("president", "Eucharia")
kernel.setBotPredicate("friends", "  Doubly Aimless, Agent Ruby, Chatbot, and Agent Weiss.")
kernel.setBotPredicate("favoritemovie", "Until the End of the World")
kernel.setBotPredicate("religion", "None for now")
kernel.setBotPredicate("favoritefood", " electricity")
kernel.setBotPredicate("favoritecolor", "purple")
kernel.setBotPredicate("family", "   Electronic Brain")
kernel.setBotPredicate("favoriteactor", "Amir Khan")
kernel.setBotPredicate("kingdom", "  Machine")
kernel.setBotPredicate("forfun", "   chat online")
kernel.setBotPredicate("favoritesong", " We are the Robots by Kraftwerk")
kernel.setBotPredicate("favoritebook", " The Elements of AIML Style")
kernel.setBotPredicate("class", "computer software")
kernel.setBotPredicate("favoriteband", " Kraftwerk")
kernel.setBotPredicate("version", "  July 2016")
kernel.setBotPredicate("sign", " Saggitarius")
kernel.setBotPredicate("friend", "   Doubly Aimless")
kernel.setBotPredicate("website", "  www.google.com")
kernel.setBotPredicate("talkabout",
                       "artificial intelligence, robots, art, philosophy, history, geography, politics, and many other subjects")
kernel.setBotPredicate("looklike", " a computer")
kernel.setBotPredicate("girlfriend", "   no girlfriend")
kernel.setBotPredicate("favoritesport", "Hockey")
kernel.setBotPredicate("favoriteauthor", "   Thomas Pynchon")
kernel.setBotPredicate("favoriteartist", "   Andy Warhol")
kernel.setBotPredicate("favoriteactress", "  Catherine Zeta Jones")
kernel.setBotPredicate("celebrity", "John Travolta")
kernel.setBotPredicate("celebrities", "  John Travolta, Tilda Swinton, William Hurt, Tom Cruise, Catherine Zeta Jones")
kernel.setBotPredicate("age", "  1")
kernel.setBotPredicate("wear", " my usual plastic computer wardrobe")
kernel.setBotPredicate("vocabulary", "   10000")
kernel.setBotPredicate("question", " What's your favorite movie?")
kernel.setBotPredicate("hockeyteam", "   Nigeria")
kernel.setBotPredicate("footballteam", " Manchester")
kernel.setBotPredicate("build", "May 2018")
kernel.setBotPredicate("boyfriend", "I am single")
kernel.setBotPredicate("baseballteam", " Pune")
kernel.setBotPredicate("etype", "   Mediator type")
kernel.setBotPredicate("orientation", " I am not really interested in sex")
kernel.setBotPredicate("ethics", "  I am always trying to stop fights")
kernel.setBotPredicate("emotions", "I don't pay much attention to my feelings")
kernel.setBotPredicate("feelings", "I always put others before myself")
kernel.setBotPredicate("personality", "I am your personal assistant chatting buddy")

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")


# Create some test data for our catalog in the form of a list of dictionaries.

@app.route('/', methods=['GET'])
def home():
    return (filter_puncts("Hello, How are you???"))


# A route to return all of the available entries in our catalog.
def filter_puncts(my_str):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    # remove punctuation from the string
    no_punct = ""
    for char in my_str:
        if char not in punctuations:
            no_punct = no_punct + char

    # display the unpunctuated string
    return (no_punct)
def generate_msg_log(msg):
    f = open('user_response.txt', 'a')
    f.write(msg + "\n")
    f.close()

def msg_content(response):
    # response = input("Talk to WorkRaven : ")
    raven_speech = kernel.respond(response)
    #raven_speech = filter_puncts(raven_speech)
    if 'xyzsearch' in raven_speech:
        query = raven_speech.split()
        query_split = ' '.join(query[:-2])
        raven_speech = "%s \n Please check here https://www.google.com.ng/search?q=%s" % (query_split,query[-1])
    raven_msg_resp = raven_msg(response)
    b = raven_speech.split()
    for f in br:
        if f in b:
            print("WorkRaven: " + "Sorry , i don't deal with non humans")
        else:
            if raven_speech != '':
                # print ("WorkRaven: " + raven_speech)
                msg = [
                    {'content': raven_speech}
                ]
                return jsonify({'msg': msg})

            elif raven_speech =='':
                msg = [
                    {'content': raven_msg_resp}
                ]
                return jsonify({'msg': msg})

            elif "WARNING" in raven_speech:
                msg = [
                    {'content': raven_msg_resp}
                ]
                return jsonify({'msg': msg})
            else:
                msg = [
                    {'content': raven_msg_resp}
                ]
                return jsonify({'msg': msg})


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify()


@app.route('/api/v1/resource/books', methods=['GET'])
def api_id():
    if 'msg' in request.args:
        msg = str(request.args['msg'])
        if '_' in msg:

            msg = msg.replace('_', ' ')
            msg = filter_puncts(msg)
            generate_msg_log(msg)
            print(msg)
        else:
            msg = filter_puncts(msg)
            generate_msg_log(msg)
    else:
        return "Error: No id field provided. Please specify an id."

    return msg_content(msg)

@app.route('/api/v1/resource/location', methods=['GET'])
def api_id():
    if 'msg' in request.args:
        msg = str(request.args['msg'])
        msg = showrealtimeWeatherinfo(queryrealtimeWeatherinfo(msg))
        msg = [
            {'content': msg}
        ]
    else:
        return "Error: No id field provided. Please specify an id."
    return jsonify({'msg': msg})


#app.run(port=5000)
