from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def mathStuff(sentence):
    response=""
    bot = ChatBot(
        'Math & Time Bot',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation',
            #'chatterbot.logic.TimeLogicAdapter'
        ]
    )  

    try:
        response=str(bot.get_response(sentence) )  
    except:   
        response ="bara zamer" 
    return response 
