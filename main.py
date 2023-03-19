import numpy as np
import pandas as pd
from tkinter import *
   
# Вывод информации о погоде на определенную дату          
def weather_on_date():
    input_date = date_entry.get()
    if input_date != '':
        weather_on_date_text.config(state='normal')
        weather_on_date_text.delete('1.0', END)
        
        date_for_df = f'{int(input_date):02}.01.2023'
        part_df = df[df['Дата'] == date_for_df]
        
        # Вывод параметров каждые 6 часов суток
        for i in range(4): 
            weather_on_date_text.insert('end', f"Погода в {(i * 6):02}:00:\n")
            row = part_df[df['Время'] == f"{(i * 6):02}:00"]
            
            for (columnName, columnData) in row.items():
                weather_on_date_text.insert('end', f"    {columnName}: {' '.join(str(x) for x in columnData.values)}\n")
                
            weather_on_date_text.insert('end', "\n")
            
    weather_on_date_text.configure(state='disabled')                


def avg_temps():
    avg_temps_text.config(state='normal')
    avg_temps_text.delete('1.0', END)
    
    for i in range(1, 32):
        date_df = df[df['Дата'] == f"{i:02}.01.2023"]
        avg_temps_text.insert('end', f"Средняя температура за {i:02}.01.2023: {np.average(date_df['Температура']):.2f}\n")
            
    avg_temps_text.configure(state='disabled')  
    
                               
# Чтение данных из файла .csv и занесение их в Dataframe
df = pd.read_csv("jan_weather.csv", encoding='ansi', sep=';', comment='#', usecols=list(range(13)))

# Разделение столбца "Местное время" на столбцы "Дата" и "Время"
df[['Дата', 'Время']] = df['Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)'].str.split(pat=' ', expand=True)
df = df.drop('Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)', axis=1)
cols_to_move = ['Дата', 'Время']
df = df[cols_to_move + [col for col in df.columns if col not in cols_to_move]]

# Переименование столбцов
df.set_axis(['Дата', 'Время', 'Температура', 'Атм. давление', 'Атм. давление на уровне моря', 'Отн. влажность', 'Напр. ветра', 'Cкорость ветра', 'Макс. порыв ветра', 'Погода', 'Явления предшествующей погоды', 'Видимость', 'Горизонтальная дальность видимости', 'Точка росы'], axis=1, inplace=True)
print(df)

root = Tk()
root.geometry("1080x720")

# Интерфейс вывода информации о погоде на определенную дату
Label(text="Информация о погоде за:").grid(row=0, column=0)
date_entry = Entry()
date_entry.grid(row=0, column=1)
Label(text=".01.2023").grid(row=0, column=2)
button = Button(text='Запросить', command=weather_on_date)
button.grid(row=0, column=3)
weather_on_date_text = Text(root, state='disabled')
weather_on_date_text.grid(row=1, column=0)

# Интерфейс вывода информации о средней ежедневной температуре за месяц
Label(text="Средняя температура за каждый день:").grid(row=2, column=0)
button = Button(text='Показать', command=avg_temps)
button.grid(row=2, column=1)
avg_temps_text = Text(root, state='disabled')
avg_temps_text.grid(row=3, column=0)



root.mainloop()
