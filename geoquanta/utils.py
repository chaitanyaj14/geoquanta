"""This is the utils module that contains the utility functions for the geoquanta package.
"""

def csv_to_df(csv_file):
    """
    Reads a CSV file and returns a pandas DataFrame.

    Args:
      csv_file (str): The path to the CSV file.

    Returns:
      pandas.DataFrame: A DataFrame containing the CSV data.
    """
    import pandas as pd
    
    return pd.read_csv(csv_file)