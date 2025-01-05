from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():
    return "Hello from the Home route!"

@home_bp.route("/about")
def about():
    return "This is the About page!"
