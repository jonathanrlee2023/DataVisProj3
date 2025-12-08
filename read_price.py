import pandas as pd

def read_price(filename):
    df = pd.read_csv(filename)
    df = df[["Year", "Jan"]]
    return df