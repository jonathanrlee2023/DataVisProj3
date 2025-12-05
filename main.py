import pandas as pd
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv("Obesity.csv")
    df = df.dropna(subset=["Data_Value"])
    # make sure all the statistics are just by age

    df = df[df["StratificationCategoryId1"] == "AGEYR"]

    df = df[["YearStart", "YearEnd", "LocationAbbr", "LocationDesc", "Datasource", "Class", "Question", "Data_Value", "Sample_Size", "Stratification1"]]
    df = df.reset_index(drop=True)
    pd.set_option('display.max_colwidth', None)

    print(df.head(10))
    print(len(df))
    print(df["Data_Value"].max())
