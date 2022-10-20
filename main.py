import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, date, timedelta
import numpy as np


def load_data(filename):
    # Use a breakpoint in the code line below to debug your script.
    return pd.read_csv(filename)


def transform(saki_db) -> pd.DataFrame:
    saki_db['time'] = saki_db['time'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M'))
    saki_db['date'] = saki_db['time'].apply(lambda x: x.date())
    return saki_db


def plot_business(saki_db):
    start_date = saki_db['time'].iloc[0].date()
    end_date = saki_db['time'].iloc[-1].date()
    duration = (end_date - start_date).days
    # business = {}
    # 1. get number of rows of pandas dataframe with correct date and business
    date, pee, poo, accident, skin, walk = [], [], [], [], [], []
    for day in range(1, duration+1):
        date_this = start_date + timedelta(day)
        day_df = saki_db[(saki_db['date'] == date_this)]
        date.append(date_this.strftime('%m/%d'))
        pee.append(len(day_df[day_df['history'].isin(['Pee', 'Pee and Poop'])]))
        poo.append(len(day_df[day_df['history'].isin(['Poop', 'Pee and Poop'])]))
        accident.append(len(day_df[day_df['history'] == 'Accident']))
        skin.append(len(day_df[day_df['history'] == 'Skin']))
        walk.append(len(day_df[day_df['history'].isin(['Walk', 'Excursion'])]))

    fig = plt.subplots()
    barWidth = 0.17
    x1 = np.arange(len(date))
    x2 = [x + barWidth for x in x1]
    x3 = [x + barWidth for x in x2]
    x4 = [x + barWidth for x in x3]
    x5 = [x + barWidth for x in x4]
    plt.bar(x1, pee, color='r', width = barWidth,
            edgecolor = 'grey', label = 'Pee')
    plt.bar(x2, poo, color='g', width = barWidth,
            edgecolor = 'grey', label = 'Poo')
    plt.bar(x3, walk, color='y', width = barWidth,
            edgecolor = 'grey', label = 'Walk')
    plt.bar(x4, skin, color='c', width = barWidth,
            edgecolor = 'grey', label = 'Skin treatment')
    plt.bar(x5, accident, color='b', width = barWidth,
            edgecolor = 'grey', label = 'Accident')
    plt.xlabel('Date', fontweight ='bold', fontsize=15)
    plt.ylabel('Number per day', fontweight='bold', fontsize=15)
    plt.xticks([r + 2*barWidth for r in range(len(date))], date)
    plt.legend()
    plt.grid()
    plt.show()

#     getting time since previous business for accidents
    duration = []
    accidents = [0] + saki_db.index[saki_db['history'] == 'Accident'].tolist()
    for i in range(len(accidents)-1):
        incident_df = saki_db.iloc[accidents[i]:accidents[i+1], :]
        prev_bus = incident_df[incident_df['history'].isin(['Pee', 'Poop', 'Pee and Poop'])].iloc[-1]
        duration.append((saki_db.iloc[accidents[i+1]]['time'] - prev_bus['time']).total_seconds()/3600)
    print(duration)


def main(filename):
    saki_db = load_data(filename)
    saki_db = transform(saki_db)
    plot_business(saki_db)
    # print(saki_db.head(15))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('sakibase.csv')
