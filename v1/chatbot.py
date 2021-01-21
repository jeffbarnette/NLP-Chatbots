import random
import json
import pickle
import time
from datetime import datetime

import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot.h5')

bot_name = 'ChatBot'

default_responses = [
    "I'm sorry, I don't understand.", "Hmm. I'm not sure.",
    "Sorry. I'm not sure what you mean.", "I don't understand.",
    "What do you mean?", "Huh?", "?", "What does that mean?",
    "I don't quite understand what you mean.",
    "That doesn't make sense to me. Please restate.",
    "That is not very clear. Please restate."
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
    if probability > 0.90:
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

def get_part_of_day(hour):
    return (
        "morning" if 1 <= hour <= 11
        else
        "afternoon" if 12 <= hour <= 17
        else
        "evening" if 18 <= hour <= 24
        else
        "evening"
    )

def process_placeholders(response, user_name):
    # Time of day
    if '<time_of_day>' in response:
        h = datetime.now().hour
        response = response.replace('<time_of_day>', get_part_of_day(h))

    # Current Time
    if '<current_time>' in response:
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        response = response.replace('<current_time>', str(current_time))
    
    # Bot name
    if '<bot_name>' in response:
        response = response.replace('<bot_name>', bot_name)
    
    # User's name
    if '<user_name>' in response:
        response = response.replace('<user_name>', user_name)

    return response

def check_context_for_user(message, context_state, user_name):
    if context_state and context_state == 'what_name':
        # Remember the user's name
        filtered_message = message.replace('you can', '')
        filtered_message = filtered_message.replace('call me', '')
        filtered_message = filtered_message.replace('my name is', '')
        filtered_message = filtered_message.strip()
        user_name = filtered_message
        message = "my name is"
    return message, user_name

def chat():
    print("Bot is running... type 'goodbye' to end chat\n")
    
    context_state = None
    user_name = ''

    # Initial greeting
    ints = predict_class('hello')
    res, context_state = get_response(ints, intents, context_state)
    res = process_placeholders(res, user_name)
    print(f"\nBot: {res}\n")

    while True:
        message = input("You: ")
        if message != '':
            message, user_name = check_context_for_user(message, \
                context_state, user_name)
            ints = predict_class(message)
            res, context_state = get_response(ints, intents, context_state)
            res = process_placeholders(res, user_name)
        else:
            res = random.choice(default_responses)

        # Simulate a typing delay 2-6 seconds
        time.sleep(random.randint(2, 7))
        print(f"\nBot: {res}\n")

        # End chat session
        if 'bye' in res.lower():
            quit()

if __name__ == '__main__':
    chat()