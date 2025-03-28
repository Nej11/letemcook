import os
from flask import Flask, render_template, request
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
    model = genai.GenerativeModel('gemini-1.5-pro')

except Exception as e:
    print(f"❌ API Initialization Error: {e}")
    model = None

def generate_recipes(ingredients):
    """Generates recipes based on provided ingredients."""
    if not model:
        return "⚠️ Recipe service is unavailable. Please try again later."
    
    prompt = f"""Generate 2-3 detailed recipes using primarily these ingredients: {', '.join(ingredients)}.
    For each recipe, provide:
    1. Name (🌟 Creative title)
    2. Prep Time / Cook Time
    3. Serving Size
    4. Ingredients (bullet points)
    5. Step-by-Step Instructions (numbered)
    6. Tips/Variations

    Format in clear markdown with ## headings. If ingredients are insufficient, 
    suggest 1-2 affordable additions.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text if response else "⚠️ No recipes generated."
    except Exception as e:
        print(f"❌ Recipe Generation Error: {e}")
        return "⚠️ Recipe generation failed. Please try different ingredients."

@app.route("/", methods=['GET', 'POST'])
def index():
    recipes = None
    if request.method == 'POST':
        ingredients = request.form.get('ingredients', '').strip()
        if not ingredients:
            return render_template('index.html', error="⚠️ Please enter some ingredients.")

        ingredient_list = [i.strip() for i in ingredients.split(',') if i.strip()]
        recipes = generate_recipes(ingredient_list)
    
    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
