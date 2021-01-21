import random
import json
import pickle

import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, jsonify

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot.h5')

default_responses = [
    "?", "Sorry. I do not understand.",
    "Sorry. I'm not sure what you mean."
]

def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json, context_state):
    tag = intents_list[0]['intent']
    probability = float(intents_list[0]['probability'])
    # Should be 90% or more certain of intent
    if probability >= 0.90:
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                if 'context_filter' not in i or 'context_filter' in i \
                    and i['context_filter'] == context_state:
                    if 'context_set' in i:
                        context_state = i['context_set']
                    else:
                        context_state = None
                    result = random.choice(i['responses'])
                    break
                else:
                    # Respond with not understood message
                    result = random.choice(default_responses)
                    break
    else:
        # Respond with not understood message
        result = random.choice(default_responses)
    return result, context_state

def chatbot_response(message, context_state):
    if message != '':
            ints = predict_class(message)
            res, context_state = get_response(ints, intents, context_state)
    else:
        res = random.choice(default_responses)
    
    response = {
        "message": res,
        "context_state": context_state
    }
    return response

app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/bot',  methods=['POST'])
def bot_response():
    if request.method == 'POST':
        content = request.json
        message = content['message']
        context_state = content['context_state']
        return jsonify(chatbot_response(message, context_state))

if __name__ == '__main__':
    app.run()