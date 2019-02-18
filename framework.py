# things we need for NLP
import nltk
from spellchecker import SpellChecker
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import FrenchStemmer

stemmer = LancasterStemmer()
fstemmer = FrenchStemmer()


def engilsh_french_stem(sentence):
    french=fstemmer.stem(sentence)
    english=stemmer.stem(sentence)
    return french if len(french)< len(english) else english

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

# restore all of our data structures
import pickle
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents file
import json
with open('intents.json') as json_data:
    intents = json.load(json_data)

spell = SpellChecker()


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
        
    #Spelling correction
    misspelled=spell.unknown(sentence_words)
    for i in sentence_words:
        if i  in misspelled:
            sentence_words[sentence_words.index(i)]=spell.correction(i)
        
    
    # stem each word
    sentence_words = [engilsh_french_stem(word.lower()) for word in sentence_words]

    #print("after cleaning up ",sentence_words)
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words):
    # clean up the sentence
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                break
                
    return(np.array(bag))    




# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')    

# load our saved model
model.load('./model.tflearn')


# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.25
def classify(sentence): # Sentence = a pattern = what user can say.
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list 


#-----------------------------------------------------------------------------------------------------------------


from watson_developer_cloud import LanguageTranslatorV3
import json

language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    iam_apikey='6N2fgkLzRaDtj7vM90uDNYiBZY8rxYRdfzXKvQ0vqio9',
    url='https://gateway-lon.watsonplatform.net/language-translator/api'
)

#-----------------------------------------------CORECTION-----------------------------------------------------
def correct(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
        
    #Spelling correction
    misspelled=spell.unknown(sentence_words)
    for i in sentence_words:
        if i  in misspelled:
            sentence_words[sentence_words.index(i)]=spell.correction(i)
    return ' '.join(sentence_words) 

#------------------------------------------------------------------------------------------------------------

def ibm_watson_translation(sentence):
    sentence=correct(sentence)
    translation = language_translator.translate(
    text=sentence,
    model_id='en-fr').get_result()
    return translation["translations"][0]["translation"]


# We will classify the pattern (sentence) and from the given intent we choose randomly a response
def response(sentence, userID='123', show_details=False):
    for i in intents['intents']:
        if 'context_filter' in i and len(context)>0 and i["context_filter"]==context[userID]:
            context.clear()
            # Check if it is a TRANSALATION
            if i["context_filter"]=="ibm_translation":
                return str(ibm_watson_translation(sentence))
            return str(random.choice(i['responses']))

    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]: # beacause the first one has the biggest propability :
                    # example : [('hours', 0.51048607), ('greeting', 0.4889779)]
                    
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        #print(random.choice(i['responses']), "  ---->   hahi il reponse ya baba hhhhh")
                        return random.choice(i['responses'])

            results.pop(0)


a=response("hello u")
print(a)            

