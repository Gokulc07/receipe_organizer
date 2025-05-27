from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'recipes.json'

def load_recipes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_recipes(recipes):
    with open(DATA_FILE, 'w') as file:
        json.dump(recipes, file, indent=4)

@app.route('/')
def index():
    recipes = load_recipes()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        recipes = load_recipes()
        recipes.append({
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions
        })
        save_recipes(recipes)
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:index>')
def delete(index):
    recipes = load_recipes()
    if 0 <= index < len(recipes):
        recipes.pop(index)
        save_recipes(recipes)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
