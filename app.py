from flask import Flask, render_template, request, jsonify
from weather_service import *

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/weather", methods=["GET"])
def weather():
    city_name = request.args.get("city")
    weather_data = get_weather_by_city(get_location_key(city_name))
    if weather_data:
        return jsonify({
            "status": "success",
            "data": weather_data
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Не удалось получить данные о погоде"
        }), 500


@app.route("/check-weather", methods=["POST"])
def check_weather():
    start_city = request.form.get("start_city").strip()
    end_city = request.form.get("end_city").strip()

    if not start_city or not end_city:
        result = "Нужно заполнить оба поля."
        return render_template("index.html", result=result)

    try:
        start_weather = get_weather_by_city(start_city)
        end_weather = get_weather_by_city(end_city)

        start_status = check_bad_weather(
            start_weather["temperature"],
            start_weather["wind_speed"],
            start_weather["precipitation_probability"]
        )
        end_status = check_bad_weather(
            end_weather["temperature"],
            end_weather["wind_speed"],
            end_weather["precipitation_probability"]
        )

        return render_template(
            'result.html',
            start_city=start_city,
            end_city=end_city,
            start_details=start_status,
            end_details=end_status
        )

    except ValueError as e:
        result = "Город не найден. Проверьте ввод."
    except requests.exceptions.ConnectionError:
        result = "Ошибка подключения к API."

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
