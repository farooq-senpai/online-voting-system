from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User, Party
from auth import auth as auth_blueprint
from voting import voting as voting_blueprint

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_blueprint)
app.register_blueprint(voting_blueprint)

@app.route('/')
def home():
    return render_template('home.html')

# Initialize DB
with app.app_context():
    db.create_all()
    # Check if we need to seed parties? user requirement says "Minimum 8 political parties must exist"
    # It might be good to auto-seed if empty.
    if Party.query.count() < 8:
        pass # We will let manual registration handle it or seed via script if needed. 
             # Requirement says "Parties are real-time entities. Party list updates dynamically"
             # So likely manual registration is preferred.

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
