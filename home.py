from flask import Flask, render_template
from flask_login import LoginManager, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'voicebot'
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return None

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)