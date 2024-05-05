import pandas as pd # type: ignore

def gen(df, filename):
    try:
        if isinstance(df, pd.DataFrame):
            path = "outputs/" + filename
            df.to_excel(path, index=False)
            return (f"'{filename}' generated successfully.")
        else:
            return ("Error: Input is not a pandas DataFrame.")
    except Exception as e:
        return (f"An error occurred while generating Excel file: {e}")
