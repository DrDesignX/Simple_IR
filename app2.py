import os
import pandas as pd
from utils import stem, calculator, config, stopword, gen_ecxel
from flask import Flask, jsonify,render_template,request  # type: ignore

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('view/index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file has been selected!'

    file = request.files['file']

    if file.filename == '':
        return 'No file selected!'
        
    # Save the file to the desired location
    file.save('uploads/' + file.filename)
   
    return 'File successfully uploaded!'



@app.route('/word_count', methods=['GET'])
def get_word_count():
    directory = config.DATA_URL
    stopwords = stopword.load()
    documents = parse_text(directory)
    stem_data = [stem.process_text(document, stopwords) for document in documents]
    word_count_list = create_word_count_list(stem_data)
    return jsonify(word_count_list)

@app.route('/tf_matrix', methods=['GET'])
def get_tf_matrix():
    directory = config.DATA_URL
    stopwords = stopword.load()
    documents = parse_text(directory)
    stem_data = [stem.process_text(document, stopwords) for document in documents]
    word_count_list = create_word_count_list(stem_data)
    term_document_matrix = generate_matrix(word_count_list)
    tf_matrix = calculator.tf(term_document_matrix)
    return jsonify(tf_matrix)

@app.route('/idf_matrix', methods=['GET'])
def get_tf_matrix():
    directory = config.DATA_URL
    stopwords = stopword.load()
    documents = parse_text(directory)
    stem_data = [stem.process_text(document, stopwords) for document in documents]
    word_count_list = create_word_count_list(stem_data)
    term_document_matrix = generate_matrix(word_count_list)
    idf_matrix = calculator.idf(term_document_matrix)
    return jsonify(idf_matrix)


@app.route('/tf_idf_matrix', methods=['GET'])
def get_tf_idf_matrix():
    directory = config.DATA_URL
    stopwords = stopword.load()
    documents = parse_text(directory)
    stem_data = [stem.process_text(document, stopwords) for document in documents]
    word_count_list = create_word_count_list(stem_data)
    term_document_matrix = generate_matrix(word_count_list)
    idf_values = calculator.idf(term_document_matrix)
    tf_idf_matrix = calculator.tf_idf(term_document_matrix, idf_values)
    return jsonify(tf_idf_matrix)

def parse_text(directory):
    documents = []
    try:
        for filename in os.listdir(directory):
            if not filename.startswith("cran.all") or filename.endswith(".txt"):
                continue
            path = os.path.join(directory, filename)
            with open(path, "r") as file:
                text = file.read()
                documents += text.split(".I")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure the directory exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return documents[1:]

def create_word_count_list(stem_data):
    word_count_list = []
    for document in stem_data:
        word_count = {}
        tokens = document.split()
        for token in tokens:
            token = token.strip('.,?!";:')
            word_count[token] = word_count.get(token, 0) + 1
        if word_count:
            del word_count[next(iter(word_count))]
        word_count_list.append(word_count)
    return word_count_list

def generate_matrix(word_doc_list):
    all_words = set(stem.get_unique_words(word_doc_list))
    num_rows = len(all_words) + 1
    num_cols = len(word_doc_list) + 1
    matrix = [[0] * num_cols for _ in range(num_rows)]
    matrix[0][0] = "Words"
    for col in range(1, num_cols):
        matrix[0][col] = f"Document {col}"
    for row, word in enumerate(all_words, start=1):
        matrix[row][0] = word
        for col, word_count in enumerate(word_doc_list, start=1):
            count = word_count.get(word, 0)
            matrix[row][col] = count
    return matrix

if __name__ == "__main__":
    app.run(debug=True)
