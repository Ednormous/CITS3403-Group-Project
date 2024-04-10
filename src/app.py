from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'we_love_writing_programs_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route('/')

def home():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)
