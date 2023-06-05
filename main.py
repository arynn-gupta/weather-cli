import requests
import typer
from PyInquirer import Token, prompt, style_from_dict
from typing_extensions import Annotated

app = typer.Typer()

style = style_from_dict(
    {
        Token.Separator: "#cc5454",
        Token.QuestionMark: "#673ab7 bold",
        Token.Selected: "#cc5454",  # default
        Token.Pointer: "#673ab7 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#f44336 bold",
        Token.Question: "",
    }
)


@app.command()
def weather(city: Annotated[str, typer.Argument()]):
    API_KEY = ""
    limit = 5
    city_req = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={API_KEY}"
    )
    city_res = city_req.json()
    if len(city_res) > 0:
        extracted_cities = []
        for city in city_res:
            try:
                extracted_cities.append(
                    {
                        "name": f'{city["name"]}, {city["state"]}, {city["country"]}',
                        "value": {
                            "lat": city["lat"],
                            "lon": city["lon"],
                        },
                    }
                )
            except:
                pass
        city_question = [
            {
                "type": "list",
                "name": "city",
                "message": "Select a city : ",
                "choices": extracted_cities,
                "validate": lambda answer: "You must choose at least one city."
                if len(answer) == 0
                else True,
            }
        ]
        city_coord = prompt(city_question, style=style)["city"]
        weather_req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={city_coord['lat']}&lon={city_coord['lon']}&appid={API_KEY}"
        )
        weather_info = weather_req.json()

        coord_lon = weather_info["coord"]["lon"]
        coord_lat = weather_info["coord"]["lat"]
        weather_description = weather_info["weather"][0]["description"]
        main_temp = weather_info["main"]["temp"]
        main_feels_like = weather_info["main"]["feels_like"]
        main_temp_min = weather_info["main"]["temp_min"]
        main_temp_max = weather_info["main"]["temp_max"]
        main_pressure = weather_info["main"]["pressure"]
        main_humidity = weather_info["main"]["humidity"]
        visibility = weather_info["visibility"]
        wind_speed = weather_info["wind"]["speed"]
        wind_deg = weather_info["wind"]["deg"]
        clouds_all = weather_info["clouds"]["all"]
        timezone = weather_info["timezone"]
        location_name = weather_info["name"]

        weather_desc = f"The current weather in {location_name}, located at coordinates {coord_lat}° latitude and {coord_lon}° longitude, is characterized by {weather_description}. The temperature is around {main_temp} Kelvin, and it feels like {main_feels_like} Kelvin. The minimum and maximum temperatures are recorded at {main_temp_min} Kelvin and {main_temp_max} Kelvin, respectively. The atmospheric pressure is {main_pressure} hPa, with a humidity level of {main_humidity}%. Visibility is excellent at {visibility} meters. The wind is blowing at a speed of {wind_speed} meters per second from {wind_deg}°. The cloud cover is approximately {clouds_all}%. The local time is in the UTC+{timezone/3600} time zone."

        print("\n" + weather_desc)
    else:
        print("No city found.")


if __name__ == "__main__":
    app()
