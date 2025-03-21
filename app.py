from flask import Flask,render_template,request, session,flash,redirect,url_for
from Model.db import db,User, Achievement, UserAchievement,insert_default_achievements
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
    insert_default_achievements()

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

@app.route('/game1')
def game1():
    return render_template("User/gameOfLife.html")


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        user = User.query.filter_by(username=u).first()
        if user and user.password == p:  
            session["userid"] = user.id
            ua = UserAchievement.query.filter_by(user_id=user.id,achievement_id = 5).first()
            if not ua:
                achievement = Achievement.query.filter_by(name="First Login").first()
                ua = UserAchievement(user_id=user.id,achievement= achievement , completed = True)
                db.session.add(ua)
                db.session.commit()
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

@app.route('/profile')
def profile():
    user = get_logged_in_user()    
    return render_template("User/profile.html",user=user.to_dict())


@app.route('/achievements')
def achievements():
    user=get_logged_in_user()
    user_achievements = (
        db.session.query(UserAchievement, Achievement)
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .filter(UserAchievement.user_id == user.id)
        .all()
    )
    return render_template("User/Achievement.html", user_achievements = user_achievements )

@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login')) 


if __name__ == "__main__":
    app.run(debug = True)