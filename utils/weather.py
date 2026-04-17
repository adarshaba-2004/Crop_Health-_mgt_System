import requests

API_KEY = "YOUR_API_KEY"

def get_weather(city="Bangalore"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        return data["main"]["temp"], data["main"]["humidity"]
    except:
        return None, None