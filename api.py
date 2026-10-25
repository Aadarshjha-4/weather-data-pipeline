import requests
import mysql.connector
from datetime import datetime

connection = None
cursor = None

try:
    # 1. EXTRACT: Fetch weather data
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 30.3165,
        "longitude": 78.0322,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    weather = response.json()["current"]

    recorded_at = datetime.fromisoformat(weather["time"])
    temperature = weather["temperature_2m"]
    humidity = weather["relative_humidity_2m"]
    wind_speed = weather["wind_speed_10m"]

    print("Weather data fetched successfully!")

    # 2. LOAD: Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="weather_pipeline"
    )

    cursor = connection.cursor()

    # 3. Store raw data
    query = """
        INSERT INTO weather_raw
        (recorded_at, temperature, humidity, wind_speed)
        VALUES (%s, %s, %s, %s)
    """

    values = (
        recorded_at,
        temperature,
        humidity,
        wind_speed
    )

    cursor.execute(query, values)
    connection.commit()

    print("Weather data saved to weather_raw!")
    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity, "%")
    print("Wind speed:", wind_speed, "km/h")

except requests.RequestException as error:
    print("API ERROR:", error)

except mysql.connector.Error as error:
    print("MYSQL ERROR:", error)

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()