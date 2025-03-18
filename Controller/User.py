from flask import Blueprint

user_bp = Blueprint('user', __name__,template_folder="User") 

@user_bp.route('/home')
def homepage():
    return "home user"