import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Fetch weather data from the OpenWeather API
def get_weather_data(city):
    api_key = 'fa69e8056b8a0f361d791408320bf280'  # Replace with your actual OpenWeather API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Parse the weather data to a more usable format
def parse_weather_data(data):
    if data['cod'] != 200:
        return {'error': data.get('message', 'Error retrieving data')}
    
    weather_info = {
        'city_name': data['name'],
        'country_code': data['sys']['country'],
        'coordinate': f"{data['coord']['lat']}, {data['coord']['lon']}",
        'temp': f"{data['main']['temp']} °C",
        'pressure': f"{data['main']['pressure']} hPa",
        'humidity': f"{data['main']['humidity']}%",
        'wind_speed': f"{data['wind']['speed']} m/s",
        'wind_direction': data['wind']['deg'],
        'weather_description': data['weather'][0]['description'].capitalize(),
        'sunrise': data['sys']['sunrise'],
        'sunset': data['sys']['sunset']
    }
    return weather_info

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            raw_data = get_weather_data(city)
            data = parse_weather_data(raw_data)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
