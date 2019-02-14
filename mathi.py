from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

def mathStuff(sentence):
    bot = ChatBot(
        'Math & Time Bot',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation',
            'chatterbot.logic.TimeLogicAdapter'
        ]
    )    
    return str(bot.get_response(sentence) )  
