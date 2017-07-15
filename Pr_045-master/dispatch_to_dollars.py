import pandas as pd

DOLLAR_PER_DISPATCH = 100

df = pd.read_csv('data/police_dispatch/police_dispatch_2016.csv')
bt = pd.to_numeric(df['beat'], errors='coerce')
bt = bt.dropna()
bt = bt.astype(int)
btv = bt.value_counts()

rbts = pd.read_csv('data/beats/beat_names.csv')
rbtList = rbts['Beat'].astype(int).tolist()

btv = btv.to_frame()
btv['beat_n'] = btv.index
btv['dollars'] = btv['beat']*DOLLAR_PER_DISPATCH
btv['valid'] = btv['beat_n'].map(lambda x: x in rbtList) 
btv = btv[btv.valid == True]

brief = btv[['dollars','beat_n']]
brief = brief.reset_index()
brief.to_csv('data/police_dispatch/police_dispatch_dollars_beat.csv')
