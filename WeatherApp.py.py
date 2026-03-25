import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# API KEYS

API_KEY = "5d0283662951441f3ac7d6355cb9d7ef"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# Get Weather + AQI

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a valid city name.")
        return

    spinner_label.config(text="⏳ Getting data...")
    result_label.config(text="")
    aqi_label.config(text="")
    icon_label.config(image="")

    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}

    try:
        response = requests.get(WEATHER_URL, params=params)
        if response.status_code != 200:
            raise Exception("City not found")

        data = response.json()

        city_name = f"{data['name']}, {data['sys']['country']}"
        temp = f"{data['main']['temp']}°C"
        weather_desc = data['weather'][0]['description'].capitalize()
        humidity = f"{data['main']['humidity']}%"
        wind = f"{data['wind']['speed']} m/s"
        icon_id = data['weather'][0]['icon']

        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
        icon_data = requests.get(icon_url).content
        image = Image.open(io.BytesIO(icon_data))
        photo = ImageTk.PhotoImage(image)
        icon_label.config(image=photo)
        icon_label.image = photo

        lat = data['coord']['lat']
        lon = data['coord']['lon']
        aqi_params = {"lat": lat, "lon": lon, "appid": API_KEY}

        aqi_res = requests.get(AQI_URL, params=aqi_params).json()
        aqi_value = aqi_res["list"][0]["main"]["aqi"]

        aqi_rating = {
            1: "Good 😊",
            2: "Fair 🙂",
            3: "Moderate 😐",
            4: "Poor 😷",
            5: "Very Poor 🤢"
        }[aqi_value]

        spinner_label.config(text="")

        result_label.config(
            text=f"{city_name}\n\n"
                 f"🌡 Temperature: {temp}\n"
                 f"🌥 Weather: {weather_desc}\n"
                 f"💧 Humidity: {humidity}\n"
                 f"💨 Wind: {wind}"
        )

        aqi_label.config(text=f"🌫 AQI: {aqi_value} – {aqi_rating}")

    except Exception:
        spinner_label.config(text="")
        messagebox.showerror("Error", "Unable to retrieve data.\nCheck city name or internet.")
        result_label.config(text="")
        aqi_label.config(text="")
        icon_label.config(image="")

# UI SETUP

root = tk.Tk()
root.title("🌦 Weather & AQI App")
root.geometry("480x650")

# BACKGROUND IMAGE (AUTO RESIZE)

bg_original = Image.open("background2.jpg")
bg_photo = ImageTk.PhotoImage(bg_original)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def resize_bg(event):
    global bg_original, bg_photo
    new_width = event.width
    new_height = event.height

    resized = bg_original.resize((new_width, new_height))
    bg_photo = ImageTk.PhotoImage(resized)
    bg_label.config(image=bg_photo)

root.bind("<Configure>", resize_bg)

# Title

title_label = tk.Label(
    root, text="🌤 Your City Conditions Today 🌬",
    font=("Arial Rounded MT Bold", 22),
    bg="#ffd9b3", fg="#8a2f00"
)
title_label.pack(pady=20)

# Entry

city_entry = tk.Entry(
    root, font=("Arial", 15),
    justify='center', width=26,
    bd=0, relief="flat",
    highlightthickness=2,
    highlightbackground="#ffb066",
    highlightcolor="#ff8c1a"
)
city_entry.pack(pady=8)
city_entry.focus()

# Hover Effects

def on_enter(e): search_btn.config(bg="#cc5500")
def on_leave(e): search_btn.config(bg="#ff6a00")

search_btn = tk.Button(
    root, text="Get Weather",
    font=("Arial", 14, "bold"),
    bg="#ff6a00", fg="white",
    width=18, bd=0,
    command=get_weather
)
search_btn.pack(pady=12)
search_btn.bind("<Enter>", on_enter)
search_btn.bind("<Leave>", on_leave)

# Spinner
spinner_label = tk.Label(root, text="", font=("Arial", 12), bg="#ffcfa8", fg="#7a2b00")
spinner_label.pack()

# Weather Card
card = tk.Frame(root, bg="white", bd=0)
card.pack(pady=20, ipadx=20, ipady=20)

icon_label = tk.Label(card, bg="white")
icon_label.pack(pady=5)

result_label = tk.Label(
    card, text="", font=("Arial", 14),
    bg="white", fg="#402000", justify="center"
)
result_label.pack()

aqi_label = tk.Label(
    card, text="", font=("Arial", 14, "bold"),
    bg="white", fg="#8e0000", justify="center"
)
aqi_label.pack(pady=10)

# Footer

footer = tk.Label(
    root, text="Powered by OpenWeather API",
    font=("Arial", 10),
    bg="#ffd9b3", fg="#4a4a4a"
)
footer.pack(side="bottom", pady=15)

root.mainloop()
