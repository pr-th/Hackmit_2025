from flask import Flask,render_template,request, session,flash,redirect,url_for
from Model.db import db,User, Achievement
import os


app =Flask(__name__)
app.secret_key = "your_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "Model", "site.db") 

app.config['SQLALCHEMY_DATABASE_URI'] =  f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# hey
with app.app_context():
    db.create_all()

def get_logged_in_user():
    if "userid" not in session:
        return redirect(url_for("login"))
    return User.query.get(session["userid"])

@app.route('/')
@app.route('/home-guest')
def homepage():
    return render_template("Home.html")

@app.route('/home')
def userhomepage():
    user = get_logged_in_user()
    return render_template("User/home.html",user=user.to_dict()) 

@app.route('/about')
def about():
    return render_template("About.html")


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        user = User.query.filter_by(username=u).first()
        if user and user.password == p:  
            session["userid"] = user.id
            return redirect(url_for("userhomepage"))
        return redirect(url_for("login"))
    return render_template("Login.html")

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form.get("username")
        p = request.form.get("password")
        e = request.form.get("email")
        user = User.query.filter_by(username=u).first()
        if (not user):
            user = User(username = u , password = p,email = e)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
    else:
        flash("Username already exists! Try another one.", "danger")
    return render_template("Register.html")   

@app.route('/tipsandtricks')
def tipsandtricks():
    return render_template("User/tipsandtricks.html")   

@app.route('/profile')
def profile():
    user = get_logged_in_user()
    return render_template("User/profile.html",user=user.to_dict())

if __name__ == "__main__":
    app.run(debug = True)