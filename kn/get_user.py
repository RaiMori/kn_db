import json
import pathlib
import os

DB_PATH = f'C:/_projects/kn_monitoring/data'
test_user = 'Almudena Ruiz'
#test_user = 'Klara'
files = os.listdir(DB_PATH)

def get_rooms_history():
    history = []
    for f in files:
        with open(f'{DB_PATH}/{f}', 'r+') as f:
            content = f.read()
            content_dict = json.loads(content)
            date_label = f.name.split('/')[-1].split('.')[0]
        history.append((date_label, content_dict))
    return history
            
def get_user_dates(user, history):
    for record in history:
        label = record[0]
        useres_lst = record[1]
        for room in useres_lst:
            #print(room.values())
            if user in " ".join(*list(room.values())):
                print(f'{label}: {user}')

history = get_rooms_history()
get_user_dates(test_user, history)