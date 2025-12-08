import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from read_price import read_price

def plot_points(df):
    plt.figure(figsize=(12, 6))
    # Plot each state
    if 'LocationAbbr' not in df.columns:
        plt.plot(df["YearStart"], df["ObesityRate"], alpha=0.6, color='blue', label='Average Obesity Rate in the US')

    else:
        for state, group in df.groupby("LocationAbbr"):
            plt.plot(group["YearStart"], group["ObesityRate"], alpha=0.6, label=state)

    plt.xlabel('Year')
    plt.ylabel('Obesity Rate (%)')
    plt.title('Obesity Rate Over Time')
    plt.legend()
    plt.show()

def plot_prices(dfs):
    plt.figure(figsize=(12, 6))
    # Plot each state
    for key, df in dfs.items():
        plt.plot(df['Year'], df['Jan'], label=key) 

    plt.xlabel('Year')
    plt.ylabel('Price ($/lb)')
    plt.title('Food Prices Over Time')
    plt.legend()
    plt.show()
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

    state_result = (
        df.groupby(['LocationAbbr','YearStart'])[['Weighted','Sample_Size']]
        .apply(lambda g: 100* (g['Weighted'].sum() / g['Sample_Size'].sum()))
        .reset_index(name='ObesityRate')
    )

    result = (
        df.groupby(['YearStart'])[['Weighted','Sample_Size']]
        .apply(lambda g: 100* (g['Weighted'].sum() / g['Sample_Size'].sum()))
        .reset_index(name='ObesityRate')
    )

    result['ObesityRate'] = result['ObesityRate'].round(2)
    state_result['ObesityRate'] = state_result['ObesityRate'].round(2)

    state_result = state_result[state_result['LocationAbbr'] != 'PR']

    top10 = (
        state_result.groupby('LocationAbbr')['ObesityRate']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    top10df = state_result[state_result['LocationAbbr'].isin(top10.index)]
    top10df = top10df.reset_index(drop=True)


    bottom10 = (
        state_result.groupby('LocationAbbr')['ObesityRate']
        .mean()
        .sort_values(ascending=True)
        .head(10)
    )

    bottom10df = state_result[state_result['LocationAbbr'].isin(bottom10.index)]
    bottom10df = bottom10df.reset_index(drop=True)

    decreased_states = []
    increased_states = []
    
    
    for state, group in state_result.groupby("LocationAbbr"):

        if not ((group["YearStart"] == 2019).any() and (group["YearStart"] == 2020).any()):
            continue 
        rate_2019 = group.loc[group["YearStart"] == 2019, "ObesityRate"].iloc[0]
        rate_2020 = group.loc[group["YearStart"] == 2020, "ObesityRate"].iloc[0]

        print(rate_2019, rate_2020)
        
        if rate_2020 < rate_2019:
            decreased_states.append(state)
        else:
            increased_states.append(state)

    filtered_df = state_result[state_result['LocationAbbr'].isin(decreased_states)]
    filtered_df = filtered_df.reset_index(drop=True)
    increased_df = state_result[state_result['LocationAbbr'].isin(increased_states)]
    increased_df = increased_df.reset_index(drop=True)


    print(result)

    bread = read_price("BreadPrices.csv")
    chicken = read_price("ChickenPrices.csv")
    rice = read_price("Rice.csv")
    bananas = read_price("Bananas.csv")
    tomatoes = read_price("Tomatoes.csv")

    dfs = {
        "Bread": bread,
        "Chicken": chicken,
        "Rice": rice,
        "Bananas": bananas,
        "Tomatoes": tomatoes
    }

    plot_prices(dfs)   

    # plot_points(result)
    # plot_price_points(result)

    # https://data.cdc.gov/Nutrition-Physical-Activity-and-Obesity/Nutrition-Physical-Activity-and-Obesity-Behavioral/hn4x-zwk7/about_data
    # https://data.bls.gov/toppicks?survey=ap
    # https://finance.alot.com/personal-finance/fast-food-prices-increase-over-past-10-years--20602