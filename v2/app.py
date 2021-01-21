import random
import pickle
import warnings

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, jsonify

warnings.filterwarnings('ignore')
nltk.download('punkt', quiet=True)

# Open binary source data file
with open('v2/source_data.pkl', 'rb') as f:
    sentence_list = pickle.load(f)

def greeting_response(text):
    text = text.lower()

    bot_greetings = ['Hello!', "Hi!", "Hola!"]
    user_greetings = [
        'hi', 'hello', 'hey', 'hola', 'ahoy', 'greetings', 'howdy'
    ]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # Swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    
    return list_index

def bot_responder(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = False

    responses_found = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response += ' ' + sentence_list[index[i]]
            response_flag = True
            responses_found += 1
        if responses_found == 1:
            break
    
    if response_flag == False:
        bot_response += 'Sorry. I do not understand.'
    
    sentence_list.remove(user_input)

    return bot_response

def chatbot_response(user_input, context_state):
    user_exit_words = [
        'quit', 'exit', 'later', 'goodbye', 'bye', 'see ya', 'I got to go',
        'ciao', 'sayonara', 'farewell', 'adios', 'so long', 'see you later',
        'adieu', 'au revior', 'cheers', 'cheerio', 'take care', 'ttyl',
        'cya', 'I have to go', 'I am done talking', 'I gotta go', 'talk later',
        'talk to you later', 'I have to go now'
    ]
    bot_exit_responses = [
        'Goodbye!', 'It was nice chatting with you. Goodbye!', 'Bye for now!',
        'It was good talking to you. Bye for now!', 'Talk to you later! Bye!',
        'Chat with you later! Goodbye!'
    ]

    if user_input.lower() in user_exit_words:
        res = random.choice(bot_exit_responses)
    else:
        bot_response = greeting_response(user_input)
        if bot_response != None:
            res = bot_response
        else:
            res = bot_responder(user_input).lstrip()
    
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