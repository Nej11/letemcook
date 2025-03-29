import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Fetch API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ No Gemini API key found. Make sure to set it in the .env file.")

# Configure Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"❌ API Initialization Error: {e}")
    model = None

def generate_recipes(ingredients):
    """Generates 3 new recipes based on provided ingredients."""
    if not model:
        return "⚠️ Recipe service is unavailable. Please try again later."
    
    prompt = f"""Generate 3 new and unique detailed recipes using primarily these ingredients: {', '.join(ingredients)}.
    For each recipe, provide:
    1. Name (🌟 Creative title)
    2. Prep Time / Cook Time
    3. Serving Size
    4. Ingredients (bullet points)
    5. Step-by-Step Instructions (numbered)
    6. Tips/Variations

    Format in clear markdown with ## headings. Ensure each recipe is **different** from previous ones.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "⚠️ No recipes generated."
    except Exception as e:
        print(f"❌ Recipe Generation Error: {e}")
        return "⚠️ Recipe generation failed. Please try different ingredients."

# Home Page Route
@app.route("/")
def home():
    return render_template("home.html")

# Recipe Generator Page
@app.route("/generate_recipe", methods=['GET', 'POST'])
def generate_recipe():
    recipes = None
    ingredients = None

    if request.method == 'POST':
        ingredients = request.form.get('ingredients', '').strip()
        if not ingredients:
            return render_template('index.html', error="⚠️ Please enter some ingredients.")

        ingredient_list = [i.strip() for i in ingredients.split(',') if i.strip()]
        recipes = generate_recipes(ingredient_list)
    
    return render_template('index.html', recipes=recipes, ingredients=ingredients)

# Placeholder for Another App
@app.route("/other_app")
def other_app():
    return "<h1>Welcome to the Other App!</h1><p>This is another application.</p>"

@app.route("/generate_more", methods=['POST'])
def generate_more():
    """Handles 'Generate More' button to get 3 more unique recipes."""
    ingredients = request.form.get('ingredients', '').strip()
    if not ingredients:
        return jsonify({"error": "⚠️ Ingredients not found!"})

    ingredient_list = [i.strip() for i in ingredients.split(',') if i.strip()]
    more_recipes = generate_recipes(ingredient_list)

    return jsonify({"new_recipes": more_recipes})

if __name__ == '__main__':
    app.run(debug=True)
