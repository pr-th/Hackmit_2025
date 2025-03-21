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
                "title": "Understanding Compound Interest",
                "content": "Compound interest is the interest on interest. It allows your savings to grow exponentially over time.",
                "risk_level": 1,
                "exp": 1
            },
            {
                "title": "How to Create a Monthly Budget",
                "content": "A monthly budget helps you track income and expenses. Use the 50/30/20 rule for efficient budgeting.",
                "risk_level": 1,
                "exp": 1
            },
            {
                "title": "Introduction to Stock Market Investing",
                "content": "Stocks represent ownership in a company. Learn the basics of investing, risk management, and market trends.",
                "risk_level": 3,
                "exp": 2
            },
            {
                "title": "The Importance of an Emergency Fund",
                "content": "An emergency fund acts as a financial cushion, covering unexpected expenses like medical bills or job loss.",
                "risk_level": 1,
                "exp": 1
            },
            {
                "title": "Understanding Credit Scores",
                "content": "A credit score impacts loan approvals and interest rates. Learn how to maintain a high score and manage debt.",
                "risk_level": 2,
                "exp": 2
            },
            {
                "title": "Basics of Cryptocurrency Investing",
                "content": "Cryptocurrencies are digital assets that use blockchain technology. Understand their risks and potential rewards.",
                "risk_level": 4,
                "exp": 3
            },
            {
                "title": "How to Start Investing in Mutual Funds",
                "content": "Mutual funds pool money from investors to buy securities. They offer diversification and professional management.",
                "risk_level": 2,
                "exp": 2
            },
            {
                "title": "Real Estate Investment Strategies",
                "content": "Real estate can generate passive income and long-term wealth. Learn about rental properties, REITs, and market trends.",
                "risk_level": 3,
                "exp": 3
            },
            {
                "title": "Retirement Planning: When to Start?",
                "content": "Starting early allows your investments to grow. Consider retirement accounts like 401(k)s and IRAs.",
                "risk_level": 2,
                "exp": 3
            },
            {
                "title": "High-Risk, High-Reward Investments",
                "content": "Venture capital, options trading, and forex are high-risk but offer potential high returns. Understand before investing.",
                "risk_level": 5,
                "exp": 4
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

