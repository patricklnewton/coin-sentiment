
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

COINS = ['BTC', 'MATIC', 'ADA', 'XLM', 'ETH']

def get_coin_compound_over_time(coin):
    res = requests.get(f'http://127.0.0.1:8000/coins/{coin}')
    data = res.json()
    compound_list = []
    date_list = []
    for item in data['coins']:
        compound_list.append(item['compound'])
        date_list.append(item['date_created'])
    return compound_list, date_list

def create_plot(coin):
    comp, date = get_coin_compound_over_time(coin)
    timeseries_data = {
        'Date': date,
        'Compound': comp
    }
    dataframe = pd.DataFrame(timeseries_data, columns=['Date', 'Compound'])
    dataframe["Date"] = dataframe["Date"].astype("datetime64")
    dataframe = dataframe.set_index("Date")
    # Plot
    plt.plot(dataframe["Compound"], marker='o')
    # Labelling 
    plt.xlabel("Date")
    plt.ylabel("Compound")
    plt.title(f' {coin} Compound')
    # Display
    plt.show()



if __name__ == "__main__":
    for coin in COINS:
        create_plot(coin)




