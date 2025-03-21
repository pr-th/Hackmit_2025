from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):    
    username = db.Column(db.String(50), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) 
    exp = db.Column(db.Integer, default=0) 
    risk_level = db.Column(db.Integer, default=1) 
    last_login = db.Column(db.DateTime, default=datetime.utcnow)  
    is_admin = db.Column(db.Boolean, nullable =False , default = False)
    achievements = db.relationship('UserAchievement', back_populates='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "exp": self.exp,
            "risk_level": self.risk_level,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_admin": self.is_admin
        }


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    users = db.relationship('UserAchievement', back_populates='achievement', lazy=True)

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='achievements')
    achievement = db.relationship('Achievement', back_populates='users')

def insert_default_achievements():
    from app import app     
    with app.app_context():  
        default_achievements = [
            {"name": "First Login", "description": "Join the Journey."},
            {"name": "First Steps", "description": "Complete your first chapter."},
            {"name": "Budget Explorer", "description": "Create your first budget plan."},
            {"name": "Savings Starter", "description": "Set a savings goal."},
            {"name": "Credit Curious", "description": "Learn the basics of credit scores."},
        ]

        for achievement in default_achievements:
            existing = Achievement.query.filter_by(name=achievement["name"]).first()
            if not existing:
                new_achievement = Achievement(name=achievement["name"], description=achievement["description"])
                db.session.add(new_achievement)

        db.session.commit()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    risk_level = db.Column(db.Integer, nullable=False)
    exp =db.Column(db.Integer,nullable = False)
    interactions = db.relationship('ArticleInteraction', back_populates='article', lazy=True)

def insert_finance_articles():
    from app import app
    with app.app_context():
        finance_articles = [
            {
                "title": "Evaluating Investment Strategies: S&P 500 vs. Individual Stocks",
                "content": "Investors often debate between investing in index funds like the S&P 500 or selecting individual stocks. While individual stocks such as Chevron and JPMorgan Chase have shown impressive returns in recent years, relying solely on them carries higher risks due to market volatility. Diversifying investments across various sectors and asset classes can mitigate risks and promote long-term wealth accumulation.",
                "risk_level": 3,
                "exp": 2
            },
            {
                "title": "Global Diversification: Investing Beyond Your Home Country",
                "content": "Diversifying investments across different geographical regions can reduce portfolio risk. While domestic markets may feel more familiar, international markets, including emerging economies, offer unique growth opportunities. However, investors should be mindful of political and economic challenges in these regions and consider global funds that cover diverse sectors.",
                "risk_level": 2,
                "exp": 2
            },
            {
                "title": "Insights from Top Fund Managers: Navigating Market Volatility",
                "content": "Recent surveys indicate that fund managers are adjusting their portfolios in response to market volatility, reducing allocations in certain regions while exploring opportunities in others. This underscores the importance for individual investors to stay informed about market trends and consider professional insights when making investment decisions.",
                "risk_level": 2,
                "exp": 3
            },
            {
                "title": "Long-Term Investment Strategies: Lessons from Industry Leaders",
                "content": "Focusing on long-term investment plans rather than short-term market movements is crucial. Industry leaders advise against panic selling during market downturns and recommend maintaining a balanced portfolio to manage risk. Adapting investment strategies based on personal circumstances and simplifying complex ideas can lead to more effective wealth management.",
                "risk_level": 2,
                "exp": 3
            },
            {
                "title": "The Role of Artificial Intelligence in Modern Investing",
                "content": "Artificial Intelligence (AI) is transforming investment strategies by providing advanced tools for market analysis and decision-making. Companies investing in AI technologies are gaining recognition for their capabilities, leading to increased investor confidence. Staying updated on AI advancements can offer investors new opportunities in the evolving financial landscape.",
                "risk_level": 3,
                "exp": 3
            }
        ]

        for article in finance_articles:
            existing = Article.query.filter_by(title=article["title"]).first()
            if not existing:
                new_article = Article(
                    title=article["title"],
                    content=article["content"],
                    risk_level=article["risk_level"],
                    exp=article["exp"]
                )
                db.session.add(new_article)

        db.session.commit()


class ArticleInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    liked = db.Column(db.Boolean, nullable=False)  
    user_risk_level = db.Column(db.Integer, nullable=False)
    user_exp = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='interactions')
    article = db.relationship('Article', back_populates='interactions')

def update_article_stats(article_id):
    interactions = ArticleInteraction.query.filter_by(article_id=article_id,liked = True).all()
    if interactions:
        avg_risk_level = sum(i.user_risk_level for i in interactions) / len(interactions)
        avg_exp = sum(i.user_exp for i in interactions) / len(interactions)
        article = Article.query.get(article_id)
        article.risk_level = round(avg_risk_level)  
        article.exp = round(avg_exp)  
        db.session.commit()

