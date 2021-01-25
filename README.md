# NLP-Chatbots
A collection of Chatbots with NLP and Machine Learning

There are two versions of a chatbot included in this collection. 

- V1 is based on NLP and Deep Learning by using a trained model based on Tensorflow and NLTK libraries.

- V2 does not use a pre-trained model but instead attempts to match to the word frequency and patterns of how the words are used while still also using some basic NLP. This is built using the Scikit-Learn, Newspaper3k and NLTK libraries.

One method may be faster, more accurate and more useful than the other, depending on the type of chatbot and the types of responses that are required. These examples were created for experimentation and comparative purposes.


## Initial Setup and Installation

- Requires Python 3.8.x or later.
- It is recommended that you first setup and activate a virtual environment before installing the dependencies.

`pip install -r requirements.txt`


## V1 Chatbot

Included in V1 is **train.py** to train a model based on the data provided in **intents.json** as well as **chatbot.py** to test the model via the command line. Also a backend service (API endpoint) was also created using Flask which can be started by running **app.py**. A simple web UI created with HTML, CSS and JavaScript is included for testing.

### Training the V1 Chatbot Model

`python3 v1/train.py`

### Running the V1 Chatbot (Command Line)

`python3 v1/chatbot.py`

To quit at any time type 'goodbye'.

### Running the V1 Chatbot Service (API)

`python3 v1/app.py`

Then open your browser to http://127.0.0.1:5000
Press Control + C to quit.


## V2 Chatbot

For V2, there is just **chatbot.py** for the command line version and **app.py** for the backend service (API endpoint) which also includes a simple front-end UI to use for testing. A web scraper tool, **scrape.py** is also included for gathering the initial data to be used with the chatbot. Simply update the URLs you wish to gather information from in the list before running.

## Running the V2 Web Scraping Tool

Make sure you first update the URLs in the **source_list** list variable to point to the specific article URLs you wish to gather data from before you run the tool. This will work on blogs, news articles and other HTML and text sources.

To obtain and provide the chatbot with cleaner source text which may also give you better results, the scraping tool will pause and allow you to review the raw source text after it has gone through parsing and natural language processing.

To do this, wait for the prompt and then open **raw_data.txt** in a text editor and make any changes you want, then save the changes. You should end up with one sentence per line with no empty lines in between.

Next, return to the command line and press ENTER (or RETURN on Mac) to continue the process which saves the resulting sentence list into a binary (*.pkl) file for use with the chatbot.

`python3 v2/scrape.py`

## Running the V2 Chatbot (Command Line)

`python3 v2/chatbot.py`

To quit at any time type 'bye'.

## Running the V2 Chatbot Service (API)

`python3 v2/app.py`

Then open your browser to http://127.0.0.1:5000
Press Control + C to quit.


## Changelog

**v1.0.0**
- Initial Release
