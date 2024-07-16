import re
import json
import math
import nltk # type: ignore
import numpy as np # type: ignore
from flask import Flask, request, jsonify,render_template # type: ignore
from collections import defaultdict
from nltk.corpus import stopwords, wordnet # type: ignore
from nltk.stem import PorterStemmer # type: ignore 
from nltk.stem.snowball import SnowballStemmer  # type: ignore

def scraper():
    file_path = "cran.all.1400"
    with open(file_path, "r") as file:
        data = file.read()

    documents = []
    current_doc = {}
    lines = data.split("\n")
    
    for line in lines:
        if line.startswith(".I"):
            if current_doc:
                documents.append(current_doc)
            current_doc = {"I": int(line.split()[1])}
        elif line.startswith(".T"):
            current_doc["T"] = ""
        elif line.startswith(".A"):
            current_doc["A"] = ""
        elif line.startswith(".B"):
            current_doc["B"] = ""
        elif line.startswith(".W"):
            current_doc["W"] = ""
        else:
            if "T" in current_doc and current_doc["T"] == "":
                current_doc["T"] += line
            elif "A" in current_doc and current_doc["A"] == "":
                current_doc["A"] += line
            elif "B" in current_doc and current_doc["B"] == "":
                current_doc["B"] += line
            elif "W" in current_doc and current_doc["W"] == "":
                current_doc["W"] += line
            else:
                if "W" in current_doc:
                    current_doc["W"] += " " + line
                elif "B" in current_doc:
                    current_doc["B"] += " " + line
                elif "A" in current_doc:
                    current_doc["A"] += " " + line
                elif "T" in current_doc:
                    current_doc["T"] += " " + line

    if current_doc:
        documents.append(current_doc)
    
    return documents

# pattern = r'\.I (\d+)\n\.T\n(.*?)\n\.A\n(.*?)\n\.B\n(.*?)\n\.W\n(.*?)\n(?=\.I|\Z)'

# matches = re.findall(pattern, scraper, re.DOTALL)
documents = scraper()

# for match in matches:
#     doc_id, T, A, B, W = match
#     W = W.replace('\n', ' ') 
#     T = T.replace('\n', ' ') 
#     B = B.replace('\n', ' ') 
#     documents.append({
#         'I': int(doc_id),
#         'T': T.strip(),
#         'A': A.strip(),
#         'B': B.strip(),
#         'W': W.strip()
#     })

with open('cranfield_documents.json', 'w') as json_file:
    json.dump(documents, json_file, indent=4)


stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def preprocess_text(text):
    tokens = tokenize_text(text)
    filtered_tokens = remove_stopwords(tokens,stop_words)
    stemmed_tokens = stem_tokens(filtered_tokens)
    return stemmed_tokens

def tokenize_text(text):
    tokens = re.findall(r'\b\d+|\b\w+\b', text.lower())
    return tokens

def remove_stopwords(tokens,stop_words):
    filtered_tokens = []
    for token in tokens:
        if token not in stop_words and len(token) > 1:
            filtered_tokens.append(token)
    return filtered_tokens

def stem_tokens(tokens):
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(ps.stem(token))
    return stemmed_tokens

for document in documents:
    document['processed_words'] = preprocess_text(document['T'] + " " + document['A'] +" " +  document['B'] + " " + document['W']) 

with open('cranfield_documents_preprocessed.json', 'w') as json_file:
    json.dump(documents, json_file, indent=4)


vocabulary = set()
for document in documents:
    vocabulary.update(document['processed_words'])

vocabulary = list(vocabulary)
vocab_index = {word: idx for idx, word in enumerate(vocabulary)}

tf_matrix = defaultdict(lambda: [0] * len(vocabulary))

for document in documents:
    doc_id = document['I']
    for word in document['processed_words']:
        tf_matrix[doc_id][vocab_index[word]] += 1


for doc_id in tf_matrix:
    for i in range(len(vocabulary)):
        if tf_matrix[doc_id][i] > 0:
            tf_matrix[doc_id][i] = (math.log10(tf_matrix[doc_id][i]) + 1)



with open('tf_matrix.json', 'w') as json_file:
    json.dump(tf_matrix, json_file, indent=4)


num_documents = len(documents)
idf = [0] * len(vocabulary)

for i in range(len(vocabulary)):
    df = sum(1 for doc_id in tf_matrix if tf_matrix[doc_id][i] > 0)
    if df > 0:
        idf[i] = math.log10(num_documents / df)


with open('idf.json', 'w') as json_file:
    json.dump(idf, json_file, indent=4)

app = Flask(__name__)

with open('cranfield_documents_preprocessed.json', 'r') as json_file:
    documents = json.load(json_file)

with open('tf_matrix.json', 'r') as json_file:
    tf_matrix = json.load(json_file)

with open('idf.json', 'r') as json_file:
    idf = json.load(json_file)


stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    query_text = request.json.get('query', '')
    additional_text = request.json.get('additional_text', '')
    combined_query = query_text + ' ' + additional_text
    processed_query = preprocess_text(combined_query)
    
    vocabulary = list({word for doc in documents for word in doc['processed_words']})
    vocab_index = {word: idx for idx, word in enumerate(vocabulary)}

    query_vector = np.zeros(len(vocabulary))
    for word in processed_query:
        if word in vocab_index:
            query_vector[vocab_index[word]] += 1
    

    query_vector = np.where(query_vector > 0, np.log10(query_vector + 1), 0)


    query_tfidf = query_vector * np.array(idf)
    
    similarities = []
    for doc_id, tf_vector in tf_matrix.items():
        tfidf_vector = np.array(tf_vector) * np.array(idf)
        similarity = np.dot(query_tfidf, tfidf_vector) / (np.linalg.norm(query_tfidf) * np.linalg.norm(tfidf_vector))
        similarities.append((doc_id, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    response = []
    for doc_id, similarity in similarities:
        if similarity > 0: 
            document = next(doc for doc in documents if doc['I'] == int(doc_id))
            response.append({
                'title': document['T'],
                'word': document['W'], 
                'auther': document['A'],
                'similarity': similarity,
                'id': document['I']
            })
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)