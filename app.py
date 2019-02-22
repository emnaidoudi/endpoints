#!flask/bin/python
from flask import Flask, jsonify, Response
from mathi import *
from framework import response
from chatterbot import ChatBot
from flask_cors import CORS
from flask_pymongo import PyMongo,MongoClient
import os
from bson.json_util import dumps
import json
from model import *

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
client = MongoClient(
    "mongodb://localhost:27017/")
db = client.mydb
collection=db["intents"]

bot_answer=""
bot = ChatBot(
    'Math & Time Bot',
    logic_adapters=[
       'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter'
   ])  


#--------------------------------------INTENTS CRUD ---------------------------------------------------------

@app.route("/api/chatbot/crud/intents",methods=['POST'])
def post_intents(intents):
    try:
        collection.insert_one(intents)
        intents=db.intents.find( { },{"tag":1,"patterns":1,"responses":1,"_id":0})
        return Response(dumps(intents),status=201) # The request has succeeded and a new resource has been created as a result of it.
    except:
        return Response(status=405)


@app.route("/api/chatbot/crud/intents",methods=['GET'])
def get_intents():
    #save_to_intents(dumps(intents))
    intents=db.intents.find( { },{"tag":1,"patterns":1,"responses":1,"_id":0})
    return Response(dumps(intents)  ,mimetype='application/json',status=200)
    


@app.route("/api/chatbot/crud/intents/<string:tag>",methods=["DELETE"]) 
def delete_intent(tag):
    try:
        collection.delete_one({ "tag" : tag })
        return Response(status=200)
    except:
        return Response(status=405) #Method not allowed  


@app.route("/api/chatbot/crud/intents")
def update_intent():
    pass







#---------------------------------------TRAIN MODEL-------------------------------------------------
@app.route("/api/chatbot/train")
def train():
    train_model()
    
    return Response(status=200)
    #os.system("./model.py")
    #execfile("./filename")

#-----------------------------------------------------------------------------------------------------

@app.route("/api/chatbot/math/<string:sentence>", methods=['GET'])
def mathApi(sentence):
    return jsonify({"result":mathStuff(sentence)}) #"5 + 5"
#-----------------------------------------------------------------------------------------------------    

@app.route("/api/chatbot/basic/<string:sentence>")
def basic(sentence):
    try:
        bot_answer=str(bot.get_response(sentence))
        return jsonify({"response":bot_answer})
    except: 
        return  jsonify({"response":response(sentence)})  

    

if __name__ == '__main__':
    app.run(debug=True)


