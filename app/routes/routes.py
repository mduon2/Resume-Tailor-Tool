from flask import render_template

#might need to split this up into seperate routing files and refactor later if gets to complicated/hard to understand/organize

def home_routing():
    """
    routing for landing page
    """
    return render_template("index.html")

def login_or_signup_routing():
    """
    routing for page with login and signup options
    """
    return render_template("login_or_signup.html")

def login_routing():
    """
    routing for login page
    """
    return render_template("login/login.html")

def signup_routing():
    """
    routing for signup page
    """
    return render_template("signup/signup.html")