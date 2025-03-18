from flask import Flask,render_template
from Controller.User import user_bp
from Controller.Admin  import admin_bp
app =Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
@app.route('/home')
def homepage():
    return render_template("Home.html") 
  
@app.route('/about')
def about():
    return render_template("About.html")

@app.route('/login')
def login():
    return render_template("Login.html")   

@app.route('/register')
def register():
    return render_template("Register.html")   
if __name__ == "__main__":
    app.run(debug = True)