import os
from flask import Flask, render_template, request, jsonify,redirect
import google.generativeai as genai
from dotenv import load_dotenv
import webbrowser

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
    model = genai.GenerativeModel('gemini-1.5-pro')

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

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate_recipe", methods=['GET', 'POST'])
def generate_recipe():
    recipes = None
    ingredients = None

    if request.method == 'POST':
        ingredients = request.form.get('ingredients', '').strip()
        if not ingredients:
            return render_template('generate_recipe.html', error="⚠️ Please enter some ingredients.")

        ingredient_list = [i.strip() for i in ingredients.split(',') if i.strip()]
        recipes = generate_recipes(ingredient_list)
    
    return render_template('index.html', recipes=recipes, ingredients=ingredients)

@app.route("/generate_more", methods=['POST'])
def generate_more():
    """Handles 'Generate More' button to get 3 more unique recipes."""
    ingredients = request.form.get('ingredients', '').strip()
    if not ingredients:
        return jsonify({"error": "⚠️ Ingredients not found!"})

    ingredient_list = [i.strip() for i in ingredients.split(',') if i.strip()]
    more_recipes = generate_recipes(ingredient_list)

    return jsonify({"new_recipes": more_recipes})

@app.route("/streamlit")
def open_streamlit():
    
    streamlit_url = "http://localhost:8501"  # Update if using a different port
    webbrowser.open(streamlit_url)  # Open Streamlit in the browser
    return f"Streamlit app should open at <a href='{streamlit_url}' target='_blank'>{streamlit_url}</a>"

def receive_data():
    data = request.get_json()
    ingredients = data.get("ingredients", [])

    if not ingredients:
        return jsonify({"error": "No ingredients received"}), 400

    print("Received ingredients:", ingredients)

    # Redirect to the home page with ingredients (modify according to your app's logic)
    return jsonify({"message": "Ingredients received", "redirect_url": "/"})

if __name__ == '__main__':
    app.run(debug=True)
