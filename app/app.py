
import manage_dynamodb
from flask import Flask, request, session, make_response, redirect, url_for, redirect, render_template, g, abort, flash, Markup, send_file
from  flask_admin import Admin
import flask_login as login
import requests
from flask_sqlalchemy import SQLAlchemy
import json
import os
import boto3
import netaddr
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

@app.route('/food/feasible/recipes', methods=['GET','POST'])
def find_recipes():
    recipes_filtered = []
    feasible_recipes = {}
    feasible_recipes_length = []
    feasible_recipes_title = []

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    f = open(API.txt, r)
    API = f.read()
    number_of_recipes = request.args.get('number')
    available_ingredients = request.args.get('ingredients')
    querystring = {"number": number_of_recipes,"ranking": "1", "ignorePantry": "true", "ingredients": available_ingredients, "apiKey":API}

    response  = requests.get(url, params=querystring)
    recipes_list_length = len(response.json())
    recipes = Response(response, status=200, mimetype='application/json')

    for x in range(0, recipes_list_length):
        if ((response.json()[x]["missedIngredientCount"]) < 3):

            recipes_filtered.append(response.json()[x])
    feasible_recipes_length = len(recipes_filtered)
    recipes_missing_ingredients = {}
    recipes_used_ingredients = {}
    recipe_total_ingredients = {}

    for x in range(0, feasible_recipes_length):

         feasible_recipes_title.append(recipes_filtered[x]["title"])
         total_ingredients = []
         missing_ingredients = []
         used_ingredients = []
         item = recipes_filtered[x]["title"]
         for y in range(0, recipes_filtered[x]["missedIngredientCount"]):
             missing_ingredients.append(recipes_filtered[x]["missedIngredients"][y]["name"])


         for z in range(0, recipes_filtered[x]["usedIngredientCount"]):
             used_ingredients.append(recipes_filtered[x]["usedIngredients"][z]["name"])

         total_ingredients.append(missing_ingredients)
         total_ingredients.append(used_ingredients)
         recipe_total_ingredients[item] = total_ingredients


    return render_template('recipes.html', data = recipe_total_ingredients)


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
    