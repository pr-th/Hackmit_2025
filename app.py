from flask import Flask,render_template,request, session,flash,redirect,url_for
from Model.db import db,User, Achievement, UserAchievement,insert_default_achievements,Article,ArticleInteraction,update_article_stats,insert_finance_articles
from sklearn.neighbors import NearestNeighbors
import numpy as np
from flask_apscheduler import APScheduler
import os


app =Flask(__name__)
app.secret_key = "your_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))   
DB_PATH = os.path.join(BASE_DIR, "Model", "site.db") 

app.config['SQLALCHEMY_DATABASE_URI'] =  f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
    insert_default_achievements()
    insert_finance_articles()

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

@app.route('/articles')
def article():
    user=get_logged_in_user()    
    all_articles = Article.query.all()

    article_data = [(article.id, article.risk_level, article.exp) for article in all_articles]
    article_ids, risk_levels, exp_values = zip(*article_data) if article_data else ([], [], [])
    
    recommended_articles = []
    if article_data:
        X = np.array(list(zip(risk_levels, exp_values)))  
        
        knn = NearestNeighbors(n_neighbors=min(5, len(X)), metric="euclidean")
        knn.fit(X)
                
        distances, indices = knn.kneighbors([[user.risk_level, user.exp]])
        recommended_articles = [Article.query.get(article_ids[i]) for i in indices[0]]

    return render_template("User/article.html", all_articles=all_articles, recommended_articles=recommended_articles)

@app.route('/article/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    user =get_logged_in_user()    
    
    user_interaction = None
    if user:
        user_interaction = ArticleInteraction.query.filter_by(user_id=user.id, article_id=article_id).first()
    
    return render_template("User/article_detail.html", article=article, user_interaction=user_interaction)

@app.route('/article/<int:article_id>/like', methods=['POST'])
def like_article(article_id):
    user = get_logged_in_user()    
    if user:
        interaction = ArticleInteraction.query.filter_by(user_id=user.id, article_id=article_id).first()
        article = Article.query.get(article_id)
        total_interactions = ArticleInteraction.query.filter_by(user_id=user.id).count()
        user.risk_level = (user.risk_level * total_interactions + article.risk_level) / (total_interactions + 1)
        db.session.commit()
        if not interaction:
            new_interaction = ArticleInteraction(user_id=user.id, article_id=article_id, liked=True, user_risk_level=user.risk_level, user_exp=user.exp)
            db.session.add(new_interaction)
        else:
            interaction.liked = True  
        db.session.commit()
    return redirect(url_for('view_article', article_id=article_id))

@app.route('/article/<int:article_id>/dislike', methods=['POST'])
def dislike_article(article_id):
    user = get_logged_in_user()    
    if user:
        interaction = ArticleInteraction.query.filter_by(user_id=user.id, article_id=article_id).first()
        if not interaction:
            new_interaction = ArticleInteraction(user_id=user.id, article_id=article_id, liked=False, user_risk_level=user.risk_level, user_exp=user.exp)
            db.session.add(new_interaction)
        else:
            interaction.liked = False
        db.session.commit()
    return redirect(url_for('view_article', article_id=article_id))



if __name__ == "__main__":
    app.run(debug = True)

scheduler = APScheduler()

@scheduler.task('interval', hours=1)
def scheduled_update():
    with app.app_context():
        articles = Article.query.all()
        for article in articles:
            update_article_stats(article.id)

scheduler.init_app(app)
scheduler.start()