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

    df['Sample_Size'] = df['Sample_Size'].replace({',': ''}, regex=True).astype(float)
    df['Weighted'] = np.floor((df['Data_Value']/100.0) * df['Sample_Size'])

    result = (
        df.groupby(['LocationAbbr', 'YearStart'])[['Weighted','Sample_Size']]
        .apply(lambda g: g['Weighted'].sum() / g['Sample_Size'].sum())
        .reset_index(name='ObesityRate')
    )
    row = result.loc[result['ObesityRate'].idxmax()]
    print(row)
    