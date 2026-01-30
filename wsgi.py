from flask import Flask
from flask_session import Session
from datetime import timedelta
import os
from app.routes.routes import home_routing, login_or_signup_routing, login_routing, signup_routing

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = os.getenv("SECRET_KEY")

app.config.update(
   SESSION_TYPE = "filesystem",
   SESSION_PERMANENT  = False,
   PERMANENT_SESSION_LIFETIME = timedelta(days=1),
   SESSION_USE_SIGNER = True
)
Session(app)

@app.route('/')
def home():
    return home_routing()

@app.route("/login_or_signup")
def login_or_signup():
    return login_or_signup_routing()

@app.route("/login")
def login():
    return login_routing()

@app.route("/signup")
def signup():
    return signup_routing()

if __name__ == "__main__":
    app.run()

from app.routes.routes import tailor_resume_routing

@app.route("/tailor", methods=["POST"])
def tailor():
    return tailor_resume_routing()
