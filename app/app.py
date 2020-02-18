from flask import Flask, render_template, url_for
import manage_dynamodb
app = Flask(__name__)

posts = [
    {
        'author': 'Pippo1',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'Febraury 20, 2019'
    },
    {
        'author': 'Pluto',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'Febraury 28, 2019'
    }

]

@app.route('/food/feasible/recipes', methods=['GET'])
def find_recipes():
    recipes_filtered = []
    feasible_recipes = {}
    feasible_recipes_length = []
    feasible_recipes_title = []
    url_on_file = open("URL.txt", r)
    url = url_on_file.read()
    number_of_recipes = request.args.get('number')
    available_ingredients = request.args.get('ingredients')
    querystring = {"number": number_of_recipes,"ranking": "1", "ignorePantry": "true", "ingredients": available_ingredients, "apiKey":"aaaa"}

    response  = requests.get(url, params=querystring)
    recipes_list_length = len(response.json())
    recipes = Response(response, status=200, mimetype='application/json')

    for x in range(0, recipes_list_length):
        if ((response.json()[x]["missedIngredientCount"]) < 3):
            recipes_filtered.append(response.json()[x])
    feasible_recipes_length = len(recipes_filtered)
    recipes_missing_ingredients = {}

    for x in range(0, feasible_recipes_length):

         feasible_recipes_title.append(recipes_filtered[x]["title"])
         missing_ingredients = []
         for y in range(0, recipes_filtered[x]["missedIngredientCount"]):
             missing_ingredients.append(recipes_filtered[x]["missedIngredients"][y]["name"])
         item = recipes_filtered[x]["title"]
         recipes_missing_ingredients[item] = missing_ingredients

    return render_template('recipes.html', data = recipes_missing_ingredients)



@app.route('/home')
def home1():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title ='About')



@app.route('/createtable')
def createtable():
    manage_dynamodb.create_table()
    return "<h1>Table Created!</h1>"
    
if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0')
    