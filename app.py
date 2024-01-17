from flask import Flask, request, jsonify, render_template
import openai
from openai import OpenAI
from dotenv import dotenv_values
import json
import re

# Load configuration and set API key
config = dotenv_values('.env')

client = OpenAI(api_key=config["OPENAI_API_KEY"])

app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')

def get_colors(msg):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a color palette generating assistant. Your job is to generate color palettes that fit the theme, mood, or instructions in the prompt. List each color with its name and hex code in the format 'Color Name - #HexCode'. The palettes should be between 2 and 8 colors."},
            {"role": "user", "content": f"Convert the following verbal description of a color palette into a list of colors: {msg}"}
        ])
        content = response.choices[0].message.content

        # Updated regex pattern to match the new format 'Color Name - #HexCode'
        pattern = r'([A-Za-z\s]+)\s*-\s*(#[0-9A-Fa-f]{6})'
        colors = re.findall(pattern, content)
        return colors

    except json.JSONDecodeError:
        return ["Error: Unable to parse colors"]
    except openai.RateLimitError:
        return ["Error: Rate limit exceeded, please try again later."]
    except openai.AuthenticationError:
        return ["Error: OpenAI authentication failed. Please check your API key."]
    except openai.error.InvalidRequestError as e:
        return [f"Error: Invalid request to OpenAI: {str(e)}"]
    except openai.error.OpenAIError as e:
        return [f"Error: OpenAI Error: {str(e)}"]
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    query = data["query"]
    colors = [{"name": name, "hex": hex_code} for name, hex_code in get_colors(query)]
    return jsonify({"colors": colors})

@app.route("/")
def index():
    default_colors = [
        {"name": "Red", "hex": "#FF0000"},
        {"name": "Orange", "hex": "#FFA500"},
        {"name": "Yellow", "hex": "#FFFF00"},
        {"name": "Green", "hex": "#008000"},
        {"name": "Blue", "hex": "#0000FF"},
        {"name": "Violet", "hex": "#8B00FF"},
        {"name": "Indigo", "hex": "#4B0082"}
    ]
    return render_template("index.html", colors=default_colors)

if __name__ == "__main__":
    app.run(debug=True)
