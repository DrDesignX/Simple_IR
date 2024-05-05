import os
import pandas as pd # type: ignore
from utils import stem
from utils import calculator
from utils import config
from utils import search
from utils import stopword
from utils import gen_ecxel

stem_data = []

def parse_text(directory):
    documents = []
    try:
        for filename in os.listdir(directory):
            # print(filename)
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


def create_word_count_list():
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
    num_rows = len(all_words) + 1  # +1 for the header row
    num_cols = len(word_doc_list) + 1  # +1 for the "Words" column
    matrix = [[0] * num_cols for _ in range(num_rows)]

    # Populate the header row
    matrix[0][0] = "Words"
    for col in range(1, num_cols):
        matrix[0][col] = f"Document {col}"
    # Populate the word counts
    for row, word in enumerate(all_words, start=1):
        matrix[row][0] = word
        for col, word_count in enumerate(word_doc_list, start=1):
            count = word_count.get(word, 0)
            matrix[row][col] = count
    return matrix

def main():
    directory = config.DATA_URL
    stopwords = stopword.load()
    documents = parse_text(directory)
    for document in documents:
        stem_data.append(stem.process_text(document, stopwords))

    word_count_list = create_word_count_list()
    unique_words_list = stem.get_unique_words(word_count_list)
    
    num_unique_words = len(unique_words_list)
    print("Number of words:", num_unique_words)

    # Create a DataFrame from the list of word counts
    # unique_word_count_pairs = set((word, count) for word_count in word_count_list for word, count in word_count.items())
    # word_count_tuples = [(word, count) for word_count in word_count_list for word, count in word_count.items()]
    # word_dic = pd.DataFrame(unique_word_count_pairs, columns=["Word", "Count"])
    # word_dic = pd.DataFrame(word_count_tuples, columns=["Word", "Count"])
    # gen_ecxel.gen(word_dic, "word-data.xlsx")

    term_document_matrix = generate_matrix(word_count_list)
    term_document_matrix = pd.DataFrame(term_document_matrix[1:], columns=term_document_matrix[0])
    gen_ecxel.gen(term_document_matrix, "raw-data.xlsx")

    idf_values = calculator.idf(term_document_matrix)
    idf = pd.DataFrame(idf_values.items(), columns=["Word", "IDF"])
    gen_ecxel.gen(idf, "idf-data.xlsx")

    tf_matrix = calculator.tf(term_document_matrix)
    tf_matrix = pd.DataFrame(tf_matrix[1:], columns=tf_matrix[0])
    gen_ecxel.gen(tf_matrix, "tf-data.xlsx")

    tf_idf_matrix = calculator.tf_idf(term_document_matrix, idf_values)
    tf_idf_matrix = pd.DataFrame(tf_idf_matrix[1:], columns=tf_idf_matrix[0])
    gen_ecxel.gen(tf_idf_matrix, "tf-idf-data.xlsx")

if __name__ == "__main__":
    main()