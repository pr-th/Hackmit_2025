from flask import Blueprint

admin_bp = Blueprint('admin', __name__) 

@admin_bp.route('/home')
def homepage():
    return "home admin"