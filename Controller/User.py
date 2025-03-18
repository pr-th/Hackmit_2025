from flask import Blueprint

user_bp = Blueprint('user', __name__) 

@user_bp.route('/home')
def homepage():
    return "home user"