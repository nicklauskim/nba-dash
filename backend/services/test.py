import pandas as pd

df = pd.read_csv('~/Downloads/nbastats_2012.csv')
print(df[df['GAME_ID'] == 21201215])

df3 = pd.read_csv('~/Downloads/nbastatsv3_2012.csv')
print(df3[df3['gameId'] == 21201215])