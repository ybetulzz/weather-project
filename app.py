from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# OpenWeather API Key
API_KEY = "09cf4996f43e46d3a64f5a9fe61ee927"

@app.route("/")
def home():
    return "Weather Recommendation API is running."

@app.route("/weather")
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()

    temperature = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    # Simple recommendation logic
    if temperature < 10:
        recommendation = "It's cold, wear a coat."
    elif temperature < 20:
        recommendation = "The weather is cool, wear a light jacket."
    else:
        recommendation = "It's warm, wear light clothes."

    return jsonify({
        "city": city.lower(),
        "temperature": temperature,
        "weather": weather_desc,
        "wind_speed": wind_speed,
        "recommendation": recommendation
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
