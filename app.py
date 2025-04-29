from flask import Flask, request, render_template_string
import datetime
import logging
import requests

app = Flask(__name__)
PORT = 5000

# Logger
logging.basicConfig(level=logging.INFO)
logging.info(f"Aplikacja uruchomiona {datetime.datetime.now()}, Autor: Jan Kowalski, Port: {PORT}")

# Predefiniowana lista
cities = {
    "Polska": ["Warszawa", "Kraków"],
    "USA": ["New York", "San Francisco"]
}

# UI Template
html_template = '''
    <form method="POST">
        <label>Kraj:</label>
        <select name="country">
            {% for country in cities %}
                <option value="{{ country }}">{{ country }}</option>
            {% endfor %}
        </select>
        <label>Miasto:</label>
        <select name="city">
            {% for city in cities[country|default('Polska')] %}
                <option value="{{ city }}">{{ city }}</option>
            {% endfor %}
        </select>
        <input type="submit" value="Sprawdź pogodę">
    </form>
    {% if weather %}
        <h3>Pogoda: {{ weather }}</h3>
    {% endif %}
'''

@app.route("/", methods=["GET", "POST"])
def index():
    weather = ""
    country = "Polska"
    if request.method == "POST":
        country = request.form["country"]
        city = request.form["city"]
        response = requests.get(f"http://wttr.in/{city}?format=3")
        weather = response.text
    return render_template_string(html_template, weather=weather, cities=cities, country=country)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
