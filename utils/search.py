import pandas as pd

def search_df_by_word(df, word):
    return df[df['Words'].str.contains(word)]
