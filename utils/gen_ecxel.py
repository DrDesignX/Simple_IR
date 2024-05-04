import pandas as pd

def gen(df, filename):
    try:
        if isinstance(df, pd.DataFrame):
            df.to_excel(filename, index=False)
            print(f"Excel file '{filename}' generated successfully.")
        else:
            print("Error: Input is not a pandas DataFrame.")
    except Exception as e:
        print(f"An error occurred while generating Excel file: {e}")
