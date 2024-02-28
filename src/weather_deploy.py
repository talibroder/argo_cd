from flask import Flask, render_template, request
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()

def save_search_history(city):
    """
    Save search history to a local JSON file.

    Args:
        city (str): The name of the city for which weather data was requested.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    history_entry = {'date': today, 'city': city}

    try:
        with open('search_history.json', 'r') as file:
            history_data = json.load(file)
    except FileNotFoundError:
        history_data = []

    history_data.append(history_entry)

    with open('search_history.json', 'w') as file:
        json.dump(history_data, file)

def get_search_history():
    """
    Get search history from the local JSON file.

    Returns:
        list: List of dictionaries containing search history entries.
    """
    try:
        with open('search_history.json', 'r') as file:
            history_data = json.load(file)
    except FileNotFoundError:
        history_data = []

    return history_data

@app.route("/")
def home():
    """
    Render the home page.
    """
    bg_color = os.getenv('BG_COLOR')
    return render_template("home.html", bg_color=bg_color), 200

@app.route("/city", methods=["GET", "POST"])
def get_weather():
    """
    Handle the user's input for the city, retrieve weather data, save search history,
    and display the results.
    """
    if request.method == "POST":
        city = request.form["city"]
        try:
            data = get_api(city)
            days = data['days'][:7]
            state = data['resolvedAddress']
            save_search_history(city)
            return render_template("search_result.html",
                                   day=days, city=city, state=state), 200
        except:
            return "Invalid City. Go back and try again."

@app.route("/history")
def show_history():
    """
    Display the search history on a separate web page.
    """
    history_data = get_search_history()
    return render_template("search_history.html", history_data=history_data), 200

def get_api(city):
    """
    Get weather data for a specified city from an external API.

    Args:
        city (str): The name of the city for which weather data is requested.

    Returns:
        dict: Weather data in JSON format.
    """
    url_path = ('https://weather.visualcrossing.com/'
                'VisualCrossingWebServices/rest/services/timeline/'
                + city + '?unitGroup=metric&key=HY7GXEUM2RZVWZJ79U9UJ6ASD&format=json')
    data = requests.get(url_path).json()
    return data

if __name__ == "__main__":
    # Access the BG_COLOR environment variable and set a default value
    bg_color = os.getenv('BG_COLOR')

    app.run(host="0.0.0.0", port=5000, debug=True)

