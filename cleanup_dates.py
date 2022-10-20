import pandas as pd
from datetime import date

# fix issue with date column 
# format datetimes better


def cleanup_dates():
    today = date.today()

    cols = ['time', 'history']

    # save to csv 
    csv_current = 'sakibase.csv'
    csv_archive = 'sakibase_archive.csv' 

    df_current = pd.read_csv(csv_current)
    df_archive = pd.read_csv(csv_archive)

    # convert dates to a usable format 
    df_current['date'] = pd.to_datetime(df_current['time'], format='%Y-%m-%d').dt.date

    # get today's and not today's data in different dfs
    df_today = df_current.loc[df_current['date'] == today]
    df_not_today = df_current.loc[df_current['date'] != today]

    # concatenate not today data with archive
    df_new_archive = pd.concat([df_archive, df_not_today], ignore_index=True)

    # rewrite archive with new concatenated df
    df_new_archive.to_csv(csv_archive, mode='w', index=False, header=True, cols=cols)

    # rewrite main file with only today's date
    df_today.to_csv(csv_current, mode='w', index=False, header=True, cols=cols)
