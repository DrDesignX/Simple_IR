import pandas as pd # type: ignore

def gen(df, filename):
    try:
        if isinstance(df, pd.DataFrame):
            path = "outputs/" + filename
            df.to_excel(path, index=False)
            print(f"Excel file '{filename}' generated successfully.")
        else:
            print("Error: Input is not a pandas DataFrame.")
    except Exception as e:
        print(f"An error occurred while generating Excel file: {e}")
