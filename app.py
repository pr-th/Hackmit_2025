from flask import Flask,render_template
from Controller.User import user_bp
from Controller.Admin  import admin_bp
app =Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def homepage():
    return "home"

if __name__ == "__main__":
    app.run(debug = True)