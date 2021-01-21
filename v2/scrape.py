import warnings
import pickle

import nltk
from newspaper import Article

warnings.filterwarnings('ignore')
nltk.download('punkt', quiet=True)

def process_text(sentence_list):
    """Save text to file for manual review"""
    with open('v2/raw_data.txt', 'w') as f:
        f.writelines(sentence_list)
    
    print('Scraped data saved to raw_data.txt')
    user_response = input('Press ENTER after you have manually reviewed and cleaned up source text! ')
    if user_response == '':
        with open('v2/raw_data.txt', 'r') as f:
            new_sentence_list = f.read().splitlines()
            print('Re-loaded data...')
        return new_sentence_list

def scrape():
    print('Scraping data from sources...')

    source_list = ['https://en.wikipedia.org/wiki/Python_(programming_language)']

    for source in source_list:
        article = Article(source)
        article.download()
        article.parse()
        article.nlp()
        corpus = article.text

        # Tokenization
        print('Tokenizing sentences...')
        text = corpus
        sentence_list = nltk.sent_tokenize(text) # List of sentences

        # Save text for manual review and clean up
        sentence_list = process_text(sentence_list)

    # Write out list to a binary file
    with open('v2/source_data.pkl', 'wb') as f:
        pickle.dump(sentence_list, f)

    print('Done!')

if __name__ == '__main__':
    scrape()
    