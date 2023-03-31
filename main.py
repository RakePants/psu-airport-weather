import numpy as np
import pandas as pd
from tkinter import *
import tkinter.scrolledtext as scrtxt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
   
   
# Вывод информации о погоде на определенную дату          
def weather_on_date():
    input_date = date_entry.get()
    if input_date != '':
        weather_on_date_text.config(state='normal')
        weather_on_date_text.delete('1.0', END)
        
        # Выбор строк, соответствующих определенной дате
        date_for_df = f'{int(input_date):02}.01.2023'
        part_df = df[df['Дата'] == date_for_df]
        
        weather_on_date_text.insert('end', f"Информация о погоде за {date_for_df}\n\n")
        
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
        avg_temps_text.insert('end', f"Средняя температура за {i:02}.01.2023: {np.average(date_df['Температура']):.2f} °C\n")
            
    avg_temps_text.configure(state='disabled')  
    

# Вывод информации обо всех днях с максимальной температурой
def max_temp():
    max_temp_text.config(state='normal')
    max_temp_text.delete('1.0', END)
    
    for i in range(1, 32):
        date_df = df[df['Дата'] == f"{i:02}.01.2023"]
        max_temp_text.insert('end', f"Максимальная температура за {i:02}.01.2023: {max(date_df['Температура']):.2f} °C\n")
            
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
        fig = Figure(figsize = (10, 5),
                    dpi = 100)
        
        date_df = df[df['Дата'] == f"{int(input_date):02}.01.2023"]

        # Отрисовка графика
        plot1 = fig.add_subplot(111)
        plot1.plot(date_df['Время'], date_df["Температура"])
        plot1.set_xticklabels(date_df['Время'], rotation=45, fontsize=7)
        plot1.invert_xaxis()
        plot1.set_ylabel("Температура, °C")
        canvas = FigureCanvasTkAgg(fig, master = root)  
        canvas.draw()
        canvas.get_tk_widget().place(relx = 0.4, rely=0.4)
                          
                               
# Чтение данных из файла .csv и занесение их в Dataframe
df = pd.read_csv("jan_weather.csv", encoding='ansi', sep=';', comment='#', usecols=list(range(13)))

# Разделение столбца "Местное время" на столбцы "Дата" и "Время"
df[['Дата', 'Время']] = df['Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)'].str.split(pat=' ', expand=True)
df = df.drop('Местное время в Шереметьево / им. А. С. Пушкина (аэропорт)', axis=1)
cols_to_move = ['Дата', 'Время']
df = df[cols_to_move + [col for col in df.columns if col not in cols_to_move]]

# Переименование столбцов
df = df.set_axis(['Дата', 'Время', 'Температура', 'Атм. давление', 'Атм. давление на уровне моря', 'Отн. влажность', 'Напр. ветра', 'Cкорость ветра', 'Макс. порыв ветра', 'Погода', 'Явления предшествующей погоды', 'Видимость', 'Горизонтальная дальность видимости', 'Точка росы'], axis=1)
#print(df)

# Создание основного окна
root = Tk()
root.geometry("1080x720")
root.state('zoomed') 
root.title('Анализ погоды')
root.iconbitmap("icon.ico")

# Интерфейс вывода информации о погоде на определенную дату
Label(text="Информация о погоде за:").place(relx = 0.01, rely=0.01)
date_entry = Entry()
date_entry.place(relx = 0.01, rely=0.035)
Label(text=".01.2023").place(relx=0.06, rely=0.035)
Button(text='Запросить', command=weather_on_date).place(relx=0.11, rely=0.035)
weather_on_date_text = scrtxt.ScrolledText(root, state='disabled', height=15)
weather_on_date_text.place(relx=0.01, rely=0.066)

# Интерфейс вывода информации о средней ежедневной температуре за месяц
y2 = 0.33
Label(text="Средняя температура за каждый день:").place(relx = 0.01, rely=y2)
Button(text='Показать', command=avg_temps).place(relx = 0.15, rely=y2)
avg_temps_text = scrtxt.ScrolledText(root, state='disabled', height=15)
avg_temps_text.place(relx = 0.01, rely=y2+0.03)

# Интерфейс вывода информации обо всех днях с максимальной температурой
y3 = 0.625
Label(text="Все дни с максимальной температурой:").place(relx=0.01, rely=y3)
Button(text='Показать', command=max_temp).place(relx=0.15, rely=y3)
max_temp_text = scrtxt.ScrolledText(root, state='disabled', height=15)
max_temp_text.place(relx=0.01, rely=y3+0.03)

# Интерфейс вывода информации о минимальном давлении за месяц
Label(text="Минимальное давление за месяц:").place(relx = 0.5, rely=0.035)
Button(text='Показать', command=min_pressure).place(relx = 0.15+0.5, rely=0.035)
min_pressure_text = scrtxt.ScrolledText(root, state='disabled', height=15)
min_pressure_text.place(relx = 0.5, rely=0.066)

# Интерфейс вывода информации о погоде на определенную дату
y5 = 0.33
Label(text="График изменения температуры: ").place(relx = 0.5, rely=y5)
date_entry_graph = Entry()
date_entry_graph.place(relx = 0.5, rely=y5+0.025)
Label(text=".01.2023").place(relx = 0.55, rely=y5+0.025)
Button(text='Запросить', command=temp_plot).place(relx = 0.6, rely=y5+0.025)

root.mainloop()
