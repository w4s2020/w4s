
import manage_dynamodb
from flask import Flask, request, session, make_response, redirect, url_for, redirect, render_template, g, abort, flash, Markup, send_file
from  flask_admin import Admin
import flask_login as login
import requests
from flask_sqlalchemy import SQLAlchemy
import json
import os
import boto3
# import netaddr
import time
import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
import sys
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError, InputRequired, Length
from wtforms import fields, form
from flask_bootstrap import Bootstrap
import simplejson
import jinja2
from jinja2.utils import Markup
from flask import Response
app = Flask(__name__)

posts = [
    {
        'author': 'Arturo Padellaro',
        'title': 'Recipes for next Xmas',
        'content': 'Pasta e fagioli con cotenna.....Boooona!!!',
        'date_posted': 'Febraury 20, 2019'
    },
    {
        'author': 'Martina Santomestolo',
        'title': 'Eggs thrown under the bus',
        'content': 'Amazing recipe but do not try it while waiting at the bus stop',
        'date_posted': 'Febraury 28, 2019'
    },
    {
        'author': 'Gemma SuperChef',
        'title': 'Eat Roblox',
        'content': 'If you like Roblox so much then eat it',
        'date_posted': 'Febraury 29, 2020'
    }

]

@app.route('/food/recipes', methods=['GET','POST'])
def find_recipes():
    if request.method == "POST":

        recipes_filtered = []
        feasible_recipes = {}
        feasible_recipes_length = []
        feasible_recipes_title = []
        total = {}

        url = "https://api.spoonacular.com/recipes/findByIngredients"
        f = open('API.txt', 'r')
        API = f.read()
        number_of_recipes = 10

        available_ingredients = request.form['ingredients']
        kitchen = request.form['kitchen']
        course = request.form['course']

        querystring = {"number": number_of_recipes,"ranking": "1", "ignorePantry": "true", "ingredients": available_ingredients, "apiKey": API}
        response  = requests.get(url, params=querystring)
        recipes_list_length = len(response.json())
        recipes = Response(response, status=200, mimetype='application/json')

        for x in range(0, recipes_list_length):
            if ((response.json()[x]["missedIngredientCount"]) < 3):

                recipes_filtered.append(response.json()[x])
                feasible_recipes_length = len(recipes_filtered)
                #recipes_missing_ingredients = {}
                #recipes_used_ingredients = {}
                #total = {}

        for x in range(0, feasible_recipes_length):

            feasible_recipes_title.append(recipes_filtered[x]["title"])
            recipe_total = []
            missing_ingredients = []
            used_ingredients = []
            recipe_id = []
            item = recipes_filtered[x]["title"]
            for y in range(0, recipes_filtered[x]["missedIngredientCount"]):
                missing_ingredients.append(recipes_filtered[x]["missedIngredients"][y]["name"])


            for z in range(0, recipes_filtered[x]["usedIngredientCount"]):
                used_ingredients.append(recipes_filtered[x]["usedIngredients"][z]["name"])

            
            recipe_id.append(recipes_filtered[x]["id"])


            recipe_total.append(missing_ingredients)
            recipe_total.append(used_ingredients)
            recipe_total.append(recipe_id)


            total[item] = recipe_total


        return render_template('recipes.html', total = total)
    return render_template('find_recipes.html')



@app.route('/food/fast_menu', methods=['GET','POST'])
def fast_menu():
    if request.method == "POST":

        query = request.form['query']
        menu_list = []
        restaurant = []

        url = "https://api.spoonacular.com/food/menuItems/search"
        f = open('API.txt', 'r')
        API = f.read()
        number_of_menu = 10

        querystring = {"query": query, "number": number_of_menu, "apiKey": API}
        response  = requests.get(url, params=querystring)

        fast_menu = response.json()['menuItems']
 
        for item in fast_menu:
            menu_list.append(item['title'])
            restaurant.append(item['restaurantChain'])


        return render_template('fast_menu.html', menu_list = menu_list, restaurant = restaurant)
    return render_template('find_fast_menu.html')




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title ='About')

@app.route('/login')
def login():
    return render_template('login.html', title ='Login')

@app.route('/register')
def register():
    return render_template('register.html', title ='Register')

@app.route('/createtable')
def createtable():
    manage_dynamodb.create_table()
    return "<h1>Table Created!</h1>"
    
if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0')
    