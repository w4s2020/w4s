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

@app.route('/')
@app.route('/home')
def home():
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
    