# Импортируем библиотеку Tkinter для отрисовки графического интрефейса программы c помощью Tkinter
from tkinter import *
# Импортируем библиотеку для работы с запросами
import requests
#Библиотека для работы с датой и временем
from datetime import datetime
#Создаем метод для получения данных о погоде используя свой api-ключ
def get_weather():
    city = input_city.get()# Получаем город от пользователя
    key = 'fd37bc378a4e8c8afbcab1a399c58777'# api-ключ из личного кабинета
    url = 'http://api.openweathermap.org/data/2.5/weather' # Базовая ссылка из которой мы получим ответ в формате JSON, используем 2,5 версию, т.к. она имеет геокодирование по названию города
    params = {'appid': key, 'q': city, 'units': 'metric','lang': 'ru' } # Дополнительные парамтеры (api-ключ, город, единицины измерения - metric температура в Цельсиях, русский язык)
    result = requests.get(url, params=params) # Отправляем запрос по нашему url
    weather = result.json()  # Получаем JSON ответ по этому URL

#Добавляем проверку при не правильно введеном городе,а также непредвиденных ошибках
    if weather["cod"] == 200:
        city = f'{str(weather["name"])}' # город для которого мы получили данные
        weather_conditions = f'{str(weather["weather"][0]["description"])}' # Общая характеристика метеусловий
        temp = "Температура: " + f'{str(weather["main"]["temp"])}' + "\xb0" # Температура
        feels_like = "Ощущается как: " + f'{str(weather["main"]["feels_like"])}' + "\xb0"  # Температура по ощущениям
        humidity = "Влажность: " + f'{str(weather["main"]["humidity"])}' + "%" # Влажность
        pressure = "Давление: " + f'{str(round(((weather["main"]["pressure"])*  0.75006375541921)))}' + " мм рт.ст." # Давление из гектопаскалей переводим в мм.рт.ст.
        speed_wind = "Скорость ветра: " + f'{str(weather["wind"]["speed"])}'+" м/с" # Скорость ветра
        date_sunrise = int((weather["sys"]["sunrise"])) # Дата и время восхода солнца в unix формате
        date_sunset = int((weather["sys"]["sunset"]))# Дата и время захода солнца в unix формате
        timezone = int((weather["timezone"])) # часовой пояс +-UTC в секундах
        dttime_sunrise = "Время Восхода: "+ str(datetime.utcfromtimestamp(date_sunrise+timezone).strftime(' %H:%M:%S')) # перевод времени в привычный формат с учетом часового пояса
        dttime_sunset = "Время Захода: "+ str(datetime.utcfromtimestamp(date_sunset+timezone).strftime(' %H:%M:%S'))# перевод времени в привычный формат с учетом часового пояса
        visibility = "Видимость: " + f'{str((weather["visibility"])/1000)}'+" км" # видимость
        # Полученные данные добавляем в текстовую надпись для отображения пользователю
        info_weather['text'] = "Сегодня в городе " + city  + "\n" + weather_conditions + "\n" + temp  + "\n" + feels_like + "\n"+  humidity+"\n"+pressure+"\n" + speed_wind + "\n" + dttime_sunrise + "\n" + dttime_sunset + "\n" + visibility
    elif weather["message"] == 'city not found':
        info_weather['text'] = "Город не найден"
    else:
        info_weather['text'] = "Ошибка"
# Создаем базовое окно нашей программы
weather_window = Tk()
# Прописываем настройки окна программы
weather_window.title('Погода') # Название окна в программе
weather_window.geometry('400x450') # Задаем размер окна
weather_window.resizable(width=False, height=False) # Фиксируем размер окна
# Создаем фреймы - рамки для размещения других объектов
frame_upper = Frame(weather_window, bg='orange', bd=5) # Привязываем его к нашему окну, задаем цвет фона и толщину обводки
frame_upper.place(relx=0, rely=0, relwidth=1, relheight=0.3) # Задаем положение на форме
# И для второго фрейма ниже
frame_footer = Frame(weather_window, bg='orange', bd=5)
frame_footer.place(relx=0, rely=0.3, relwidth=1, relheight=0.8)
label_input = Label(frame_upper, bg='orange', text='Введите город:', font=30)#Заголовок для поля ввода города
label_input.pack(expand=True)# Порядок положения объектов во фрейме
input_city = Entry(frame_upper, bg='white', font=30)# Создаем поле для ввода города
#input_city.insert(0,"Введите город") хотел сделать плэйсхолдер,но в tk нормально,без костылей не реализован
input_city.pack()
btn_get = Button(frame_upper,bg='yellow', text='Запросить погоду', command=get_weather,font=30)# Создаем кнопку,прописываем положение,название и привязываем к методу get_weather
btn_get.pack(expand=True)
info_weather = Label(frame_footer, text='Данные о погоде в городе', bg='orange', font=30)# Создаем текстовое поле для вывода информации о погоде
info_weather.pack()


weather_window.mainloop()
