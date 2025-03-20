from flask import Flask,render_template
from Model.db import db,User, Achievement

app =Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\mahaj\OneDrive\Desktop\Hackmit_2025\Model\site.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# hey
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home-guest')
def homepage():
    return render_template("Home.html")

@app.route('/home')
def userhomepage():
    return render_template("User/home.html") 

@app.route('/about')
def about():
    return render_template("About.html")

@app.route('/login')
def login():
    return render_template("Login.html")   

@app.route('/register')
def register():
    return render_template("Register.html")   

@app.route('/tipsandtricks')
def tipsandtricks():
    return render_template("User/tipsandtricks.html")   

if __name__ == "__main__":
    app.run(debug = True)