import pandas as pd
import tkinter as tk

# Чтение данных из файла .csv и занесение их в Dataframe
df = pd.read_csv("jan_weather.csv", encoding='ansi', sep=';', comment='#', usecols=list(range(13)))

# Разделение столбца "Местное время" на столбцы "date" и "time"
df[['date', 'time']] = df['Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)'].str.split(pat=' ', expand=True)
df = df.drop('Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)', axis=1)
cols_to_move = ['date', 'time']
df = df[cols_to_move + [col for col in df.columns if col not in cols_to_move]]
print(df)

