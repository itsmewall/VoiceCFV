from flask import Flask, render_template
from flask_login import login_required, current_user
from auth import login_manager

app = Flask(__name__)

@app.route('/dashboard')
@login_required
def dashboard():
    login_manager.login_view = 'login'
    # Retrieve information for the current user, e.g. from a database
    user_info = {'username': current_user.username, 'email': current_user.email}

    # Render the dashboard template, passing in the user's information
    return render_template('dashboard.html', user=user_info)

if __name__ == '__main__':
    app.run(debug=True)
