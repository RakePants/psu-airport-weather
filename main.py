import numpy as np
import pandas as pd
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
   
   
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


# Вывод информации о средней ежедневной температуре за месяц (средняя температура на каждый день)
def avg_temps():
    avg_temps_text.config(state='normal')
    avg_temps_text.delete('1.0', END)
    
    for i in range(1, 32):
        date_df = df[df['Дата'] == f"{i:02}.01.2023"]
        avg_temps_text.insert('end', f"Средняя температура за {i:02}.01.2023: {np.average(date_df['Температура']):.2f}\n")
            
    avg_temps_text.configure(state='disabled')  
    

# Вывод информации обо всех днях с максимальной температурой
def max_temp():
    max_temp_text.config(state='normal')
    max_temp_text.delete('1.0', END)
    
    for i in range(1, 32):
        date_df = df[df['Дата'] == f"{i:02}.01.2023"]
        max_temp_text.insert('end', f"Максимальная температура за {i:02}.01.2023: {max(date_df['Температура']):.2f}\n")
            
    max_temp_text.configure(state='disabled')  
     
        
# Вывод информации о минимальном давлении за месяц
def min_pressure():
    min_pressure_text.config(state='normal')
    min_pressure_text.delete('1.0', END)
    
    min_pressure_text.insert('end', f"Минимальное давление, {max(df['Атм. давление'])} мм рт. ст., было: \n")
    for _, row in df.iterrows():
        if row['Атм. давление'] == min(df['Атм. давление']):
            min_pressure_text.insert('end', f"  {row['Дата']} {row['Время']}\n")
            
    min_pressure_text.configure(state='disabled') 


# Вывод графика изменения температуры в течение указанной даты
def temp_plot():
    input_date = date_entry_graph.get()
    if input_date != '':
        fig = Figure(figsize = (8, 4),
                    dpi = 100)
        
        date_df = df[df['Дата'] == f"{int(input_date):02}.01.2023"]
      
        plot1 = fig.add_subplot(111)
        plot1.plot(date_df['Время'], date_df["Температура"])
        plot1.set_xticklabels(date_df['Время'], rotation=45, fontsize=6)
        plot1.invert_xaxis()
        plot1.set_ylabel("Температура, °C")
        canvas = FigureCanvasTkAgg(fig, master = root)  
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=4)
                          
                               
# Чтение данных из файла .csv и занесение их в Dataframe
df = pd.read_csv("jan_weather.csv", encoding='ansi', sep=';', comment='#', usecols=list(range(13)))

# Разделение столбца "Местное время" на столбцы "Дата" и "Время"
df[['Дата', 'Время']] = df['Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)'].str.split(pat=' ', expand=True)
df = df.drop('Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)', axis=1)
cols_to_move = ['Дата', 'Время']
df = df[cols_to_move + [col for col in df.columns if col not in cols_to_move]]

# Переименование столбцов
df = df.set_axis(['Дата', 'Время', 'Температура', 'Атм. давление', 'Атм. давление на уровне моря', 'Отн. влажность', 'Напр. ветра', 'Cкорость ветра', 'Макс. порыв ветра', 'Погода', 'Явления предшествующей погоды', 'Видимость', 'Горизонтальная дальность видимости', 'Точка росы'], axis=1)

root = Tk()
root.geometry("1080x720")
root.state('zoomed')

# Интерфейс вывода информации о погоде на определенную дату
Label(text="Информация о погоде за:").grid(row=0, column=0)
date_entry = Entry()
date_entry.grid(row=0, column=1)
Label(text=".01.2023").grid(row=0, column=2)
Button(text='Запросить', command=weather_on_date).grid(row=0, column=3)
weather_on_date_text = Text(root, state='disabled')
weather_on_date_text.grid(row=1, column=0)

# Интерфейс вывода информации о средней ежедневной температуре за месяц
Label(text="Средняя температура за каждый день:").grid(row=2, column=0)
Button(text='Показать', command=avg_temps).grid(row=2, column=1)
avg_temps_text = Text(root, state='disabled')
avg_temps_text.grid(row=3, column=0)

# Интерфейс вывода информации обо всех днях с максимальной температурой
Label(text="Все дни с максимальной температурой:").grid(row=4, column=0)
Button(text='Показать', command=max_temp).grid(row=4, column=1)
max_temp_text = Text(root, state='disabled')
max_temp_text.grid(row=5, column=0)

# Интерфейс вывода информации о минимальном давлении за месяц
Label(text="Минимальное давление за месяц:").grid(row=0, column=4)
Button(text='Показать', command=min_pressure).grid(row=0, column=5)
min_pressure_text = Text(root, state='disabled')
min_pressure_text.grid(row=1, column=4)

# Интерфейс вывода информации о погоде на определенную дату
Label(text="График изменения температуры: ").grid(row=2, column=4)
date_entry_graph = Entry()
date_entry_graph.grid(row=2, column=5)
Label(text=".01.2023").grid(row=2, column=6)
Button(text='Запросить', command=temp_plot).grid(row=2, column=7)

root.mainloop()
