import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests as rq
import pytz
from datetime import datetime, timedelta


# window
window = tk.Tk()
window.title('Weather')
window.geometry('600x400')
window.resizable(False, False)

# layout
window.columnconfigure(0, weight=7, uniform='a')
window.columnconfigure(1, weight=1, uniform='a')
window.rowconfigure(0, weight=1, uniform='a')
window.rowconfigure((1, 2), weight=3, uniform='a')

# image
image = Image.open('C:\\Users\\Marek\\OneDrive\\Desktop\\Pers1r\\projects\\games\\bg_image_3.jpg')
bg_img = ImageTk.PhotoImage(image)
canvas = tk.Canvas(window)
canvas.grid(row=0, column=0, columnspan=10, rowspan=10, sticky='nsew')
canvas.create_image(0, 0, image=bg_img, anchor='nw')

icon = None
icon_1 = None
hours = 0


def get_weather(town):
    global icon, icon_1, hours

    api_key = '118ee1fbcd530d985af2e8ae5d333824'
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    img_link = 'http://openweathermap.org/img/wn/'

    response = rq.get(
        url=api_url,
        params={
            "q": town,
            "appid": api_key,
            "units": "metric",
        }
    )

    weather_data = response.json()
    canvas.delete('text')

    # background
    canvas.create_image(0, 0, image=bg_img, anchor='nw')
    try:
        # values
        name = weather_data['name']
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        max_temp = weather_data['main']['temp_max']
        min_temp = weather_data['main']['temp_min']

        if len(name) < 15:
            canvas.create_text(150,
                               95,
                               text=name,
                               font='Consolas 30',
                               )
        else:
            canvas.create_text(140,
                               100,
                               text=name,
                               font='Consolas 20',
                               )

        canvas.create_text(200,
                           170,
                           text='Weather',
                           font='Consolas 20',
                           )

        canvas.create_text(200,
                           200,
                           text=description,
                           font='Consolas 15',
                           )

        canvas.create_text(200,
                           230,
                           text=str(int(temp)) + '°C',
                           font='Consolas 20 bold',
                           )

        canvas.create_text(200,
                           260,
                           text=str(int(max_temp)) + '°C' + '/' + str(int(min_temp)) + '°C',
                           font='Consolas 15',
                           )

        data = rq.get(img_link + str(weather_data['weather'][0]['icon']) + '.png').content

        f = open('icon.png', 'wb')
        f.write(data)
        f.close()

        icon = tk.PhotoImage(file='icon.png')
        icon_1 = icon.zoom(3, 3)
        canvas.create_image(320, 210, image=icon_1, anchor='center')

        # time
        hours = (weather_data['timezone']) // 3600

        def update_time():
            current_time = (datetime.now(pytz.utc) + timedelta(hours=hours)).strftime('%d.%m.%Y %H:%M:%S')
            canvas.itemconfig(time_text_id, text=current_time)
            window.after(1000, update_time)

        time_text_id = canvas.create_text(400, 100, text="", font='Consolas 20')
        update_time()

    except KeyError:
        canvas.create_text(250, 200, text="Invalid city name.", font='Consolas 30', fill='red')


# entry
city = tk.StringVar(value='Type in your city...')
search = ttk.Entry(window, textvariable=city)
search.grid(row=0, column=0, sticky='nsew', padx=10, pady=15)
search.bind('<FocusIn>', lambda x: search.selection_range(0, tk.END))
image = tk.PhotoImage(file='search.png')
search_button = tk.Button(window, bd=0, cursor='hand2', image=image, command=lambda: get_weather(city.get()))
search_button.grid(row=0, column=1, sticky='w')

# searching
search.bind('<Return>', lambda x: get_weather(city.get()))

# run
window.mainloop()
