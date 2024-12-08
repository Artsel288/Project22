import requests
from config import API_KEY, BASE_URL


def get_location_key(city_name):
    url = f"{BASE_URL}/locations/v1/cities/search"
    params = {"apikey": API_KEY, "q": city_name}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["Key"]
    return None


def get_weather_forecast(location_key):
    url = f"{BASE_URL}/forecasts/v1/daily/1day/{location_key}"
    params = {"apikey": API_KEY, "metric": True}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None


def get_weather_by_city(city_name):
    """
    Получает данные о погоде по названию города через API.

    :param city_name: Название города.
    :return: Словарь с ключевыми параметрами погоды (температура, ветер, осадки).
    """
    try:
        # Запрос на получение location_key
        location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
        location_params = {"apikey": API_KEY, "q": city_name}
        location_response = requests.get(location_url, params=location_params)
        location_data = location_response.json()
        location_key = location_data[0]["Key"]

        # Запрос на получение погоды
        weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        weather_params = {"apikey": API_KEY, "details": "true"}
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()[0]

        return {
            "temperature": weather_data["Temperature"]["Metric"]["Value"],
            "wind_speed": weather_data["Wind"]["Speed"]["Metric"]["Value"],
            "precipitation_probability": weather_data.get("PrecipitationProbability", 0)
        }
    except Exception as e:
        raise ValueError(f"Failed to fetch weather data for city {city_name}: {str(e)}")


def check_bad_weather(temperature, wind_speed, precipitation_probability):
    """Оценка погодных условий и возврат детальной информации."""
    details = {
        "temperature": temperature,
        "wind_speed": wind_speed,
        "precipitation_probability": precipitation_probability,
        "conditions": "благоприятные"
    }

    # Логика определения неблагоприятных условий
    if temperature < -25 or temperature > 35:
        details["conditions"] = "неблагоприятные"
    elif wind_speed > 50:
        details["conditions"] = "неблагоприятные"
    elif precipitation_probability > 70:
        details["conditions"] = "неблагоприятные"

    return details
