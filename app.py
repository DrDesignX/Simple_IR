import os
import pandas as pd # type: ignore
from utils import stem
from utils import calculator
from utils import config
from utils import search
from utils import stopword
from utils import gen_excel

import tkinter as tk
from tkinter import filedialog

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


# A list containing dictionaries of word counts for each document.
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

# A matrix representation of the word counts, where rows represent words and columns represent documents.
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
            matrix[row][col] = int(count)
    return matrix

def generate_word_count(filename):
    path = 'outputs/' + filename
    word_count_list = create_word_count_list()

    word_count_matrix = {}
    for word_count in word_count_list:
        for word, count in word_count.items():
            if word in word_count_matrix:
                word_count_matrix[word] += count
            else:
                word_count_matrix[word] = count

    with open(path, 'w') as file:
        for word, count in word_count_matrix.items():
            file.write(f"{word}: {count}\n")
        
    return (f"'{filename}' generated successfully.")

def main():
    def select_folder():
        folder_path = filedialog.askdirectory()
        config.DATA_URL = folder_path
        folder_path_var.set(folder_path)
        root.destroy()

    root = tk.Tk()
    root.title("Choose a folder")

    window_width = 400
    window_height = 200
    root.geometry(f"{window_width}x{window_height}")
    folder_path_var = tk.StringVar()

    folder_label = tk.Label(root, textvariable=folder_path_var)
    folder_label.pack()
    select_button = tk.Button(root, text="Browse", command=select_folder)
    select_button.pack()
    root.mainloop()

    directory = config.DATA_URL
    print(directory)
    stopwords = stopword.load()
    documents = parse_text(directory)
    for document in documents:
        stem_data.append(stem.process_text(document, stopwords))
    word_count_list = create_word_count_list()

    unique_words_list = stem.get_unique_words(word_count_list)
    num_unique_words = len(unique_words_list)
    print("Number of words:", num_unique_words)

    print(generate_word_count("word_count.txt"))

    term_document_matrix = generate_matrix(word_count_list)
    term_document_matrix_df = pd.DataFrame(term_document_matrix[1:], columns=term_document_matrix[0])
    # print(term_document_matrix_df)
    gen_excel.gen(term_document_matrix_df, "raw-data.xlsx")

    # tf_matrix = calculator.tf(term_document_matrix)
    # tf_matrix_df = pd.DataFrame(tf_matrix[1:], columns=tf_matrix[0])
    # # print(tf_matrix_df)
    # gen_excel.gen(tf_matrix_df, "tf-data.xlsx")

    # idf_values_df = calculator.idf(term_document_matrix)
    # idf_df = pd.DataFrame(idf_values_df.items(), columns=["Word", "IDF"])
    # # print(idf_df)
    # gen_excel.gen(idf_df, "idf-data.xlsx")

    # tf_idf_matrix = calculator.tf_idf(term_document_matrix, idf_values_df)
    # tf_idf_matrix_df = pd.DataFrame(tf_idf_matrix[1:], columns=tf_idf_matrix[0])
    # # print(tf_idf_matrix_df)
    # gen_excel.gen(tf_idf_matrix_df, "tf-idf-data.xlsx")

if __name__ == "__main__":
    main()