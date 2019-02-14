#!flask/bin/python
from flask import Flask, jsonify
from mathi import *
from framework import response

app = Flask(__name__)



#-----------------------------------------------MATH------------------------------------------------------
@app.route("/api/chatbot/math/<string:sentence>", methods=['GET'])
def mathApi(sentence):
    return jsonify({"result":mathStuff(sentence)}) #"5 + 5"
#-----------------------------------------------------------------------------------------------------    
@app.route("/api/chatbot/basic/<string:sentence>")
def basic(sentence):
    return jsonify({"response":response(sentence)})

if __name__ == '__main__':
    app.run(debug=True)


