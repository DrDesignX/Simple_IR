# import os
# import pandas as pd # type: ignore
# from utils import stem
# from utils import calculator
# from utils import config
# from utils import search
# from utils import stopword
# from utils import gen_ecxel

# stem_data = []

# def parse_text(directory):
#     documents = []
#     try:
#         for filename in os.listdir(directory):
#             # print(filename)
#             if not filename.startswith("cran.all") or filename.endswith(".txt"):
#                 continue
#             path = os.path.join(directory, filename)
#             with open(path, "r") as file:
#                 text = file.read()
#                 documents += text.split(".I")
#     except FileNotFoundError as e:
#         print(f"Error: {e}. Please make sure the directory exists.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     return documents[1:]


# def create_word_count_list():
#     word_count_list = []
#     for document in stem_data:
#         word_count = {}
#         tokens = document.split()
#         for token in tokens:
#             token = token.strip('.,?!";:')
#             word_count[token] = word_count.get(token, 0) + 1
#         if word_count:
#             del word_count[next(iter(word_count))]
#         word_count_list.append(word_count)
#     return word_count_list

# def generate_matrix(word_doc_list):
#     all_words = set(stem.get_unique_words(word_doc_list))
#     num_rows = len(all_words) + 1  # +1 for the header row
#     num_cols = len(word_doc_list) + 1  # +1 for the "Words" column
#     matrix = [[0] * num_cols for _ in range(num_rows)]

#     # Populate the header row
#     matrix[0][0] = "Words"
#     for col in range(1, num_cols):
#         matrix[0][col] = f"Document {col}"
#     # Populate the word counts
#     for row, word in enumerate(all_words, start=1):
#         matrix[row][0] = word
#         for col, word_count in enumerate(word_doc_list, start=1):
#             count = word_count.get(word, 0)
#             matrix[row][col] = count
#     return matrix

# def main():
#     directory = config.DATA_URL
#     stopwords = stopword.load()
#     documents = parse_text(directory)
#     for document in documents:
#         stem_data.append(stem.process_text(document, stopwords))
#     word_count_list = create_word_count_list()

#     unique_words_set = set()

#     # Create a dictionary to store word counts
#     word_counts = {}

#     for dic in word_count_list:
#         for word, count in dic.items():
#             # Add word to set
#             unique_words_set.add(word)
#             # Add word to dictionary with its count
#             word_counts[word] = count
#             # Print word and its count
#             print(f"{word}, Count: {count}")


#     word_df = pd.DataFrame(word_count_list)
#     # print(word_df.head())
#     # word_df.to_excel("word_data.xlsx", index=False)

#     unique_words_list = stem.get_unique_words(word_count_list)
#     num_unique_words = len(unique_words_list)
#     print("Number of words:", num_unique_words)
#     printer=False

#     if printer:
#         term_document_matrix = generate_matrix(word_count_list)
#         term_document_matrix_df = pd.DataFrame(term_document_matrix[1:], columns=term_document_matrix[0])
#         gen_ecxel.gen(term_document_matrix_df, "raw-data.xlsx")

#         idf_values_df = calculator.idf(term_document_matrix)
#         idf_df = pd.DataFrame(idf_values_df.items(), columns=["Word", "IDF"])
#         gen_ecxel.gen(idf_df, "idf-data.xlsx")

#         tf_matrix = calculator.tf(term_document_matrix)
#         tf_matrix_df = pd.DataFrame(tf_matrix[1:], columns=tf_matrix[0])
#         gen_ecxel.gen(tf_matrix_df, "tf-data.xlsx")

#         tf_idf_matrix = calculator.tf_idf(term_document_matrix, idf_values)
#         tf_idf_matrix_df = pd.DataFrame(tf_idf_matrix[1:], columns=tf_idf_matrix[0])
#         gen_ecxel.gen(tf_idf_matrix_df, "tf-idf-data.xlsx")

# if __name__ == "__main__":
#     main()