import re
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
def process_text(text,stopwords):
    tokens = tokenize_text(text)
    filtered_tokens = remove_stopwords(tokens,stopwords)
    stemmed_tokens = stem_tokens(filtered_tokens)
    return " ".join(stemmed_tokens)

def tokenize_text(text):
    text = re.sub(r"[^\w\s]", " ", text)
    # text = ''.join(char if char.isalpha() else ' ' for char in text)
    text = text.lower()
    tokens = text.split()
    return tokens

def remove_stopwords(tokens,stopwords):
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens

def stem_tokens(tokens):
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

def get_unique_words(word_count_list):
    unique_words = set()
    for word_count in word_count_list:
        unique_words.update(word_count.keys())
    return unique_words