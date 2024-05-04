import math
import pandas as pd # type: ignore

def log_tf(tf):
    if tf == 0 or tf < 0 :
        return 0  # Logarithm of 0 is undefined
    else:
        return 1 + math.log(tf)

def tf(tf_matrix):
    for i in range(1, len(tf_matrix)):
        for j in range(1, len(tf_matrix[i])):
            tf = tf_matrix[i][j]
            tf_matrix[i][j] = log_tf(tf)
    return tf_matrix

import math

def idf(term_document_matrix):
    num_documents = len(term_document_matrix[0]) - 1  # Subtract 1 for the header row
    idf_values = {}

    for row in range(1, len(term_document_matrix)):
        word = term_document_matrix[row][0]
        doc_frequency = sum(1 for col in range(1, len(term_document_matrix[row])) if term_document_matrix[row][col] > 0)
        idf_values[word] = math.log(num_documents / (1 + doc_frequency))

    return idf_values


def tf_idf(term_document_matrix, idf_values):
    tf_idf_matrix = [["Words"] + [f"Document {i}" for i in range(1, len(term_document_matrix[0]))]]

    for row in range(1, len(term_document_matrix)):
        word = term_document_matrix[row][0]
        tf_idf_row = [word]
        for col in range(1, len(term_document_matrix[row])):
            tf = term_document_matrix[row][col]
            idf = idf_values.get(word, 0)  # If word not found in IDF values, default to 0
            tf_idf = tf * idf
            tf_idf_row.append(tf_idf)
        tf_idf_matrix.append(tf_idf_row)

    return tf_idf_matrix
