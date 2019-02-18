#!flask/bin/python
from flask import Flask, jsonify
from mathi import *
from framework import response
from chatterbot import ChatBot

app = Flask(__name__)

bot_answer=""
bot = ChatBot(
    'Math & Time Bot',
    logic_adapters=[
       'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter'
   ])  



#--------------------------------------INTENTS---------------------------------------------------------
@app.route("/api/chatbot/intents",methods=['POST'])
def fill_intents_file(intents):
    pass
#--------------------------------------------------------------------------------------------------------

#-----------------------------------------------MATH------------------------------------------------------
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


