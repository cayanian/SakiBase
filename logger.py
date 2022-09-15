import pandas as pd
import datetime
import getch 
from os.path import exists

filename = 'sakibase.csv'

cols = ['time', 'history']
history = pd.DataFrame(columns=cols)

activities = {
    '1': 'Pee',
    '2': 'Poop',
    '3': 'Pee and Poop',
    'b': 'Breakfast',
    'd': 'Dinner',
    's': 'Skin',
    'a': 'Accident',
    'v': 'Vommit',
    'w': 'Walk',
    'p': 'Play',
    'c': 'Crate',
    'e': 'Excursion'
}

def display(history):
    print(history)

# react to button
def log_activity(history, write=0, filename='test.csv'):
    keypress = getch.getKey().lower()
    now = datetime.datetime.now()

    if keypress in activities:
        decoded = activities[keypress]

        logged = pd.DataFrame([[now, decoded]], columns=cols)
        history = pd.concat([history, logged], ignore_index=True)

        display(logged.head())

        # save to csv 
        mode = 'a'
        header = False
        if not exists(filename):
            header = True
        if write:
            mode = 'w'
            header = True
        
        logged.to_csv(filename, mode=mode, index=False, header=header)

    # really slow undo
    if keypress == 'u':
        print('Undo')
        lines = []
        with open(filename, mode='r+') as f:
            lines = f.readlines()
            lines = lines[:-1]
        
        with open(filename, mode='w') as f:
            f.writelines(lines)

    # exit
    if keypress == 'x':
        print('Exit')
        return history, True


    return history, False


while 1:
    now = datetime.datetime.now()
    history, stop = log_activity(history,filename=filename)
    if stop:  
        break  
