from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from auth import User

app = Flask(__name__)
app.secret_key = "voicebot"

# Dados de usuário cadastrado (substitua por dados reais do seu banco de dados)
user = User(1, 'usuario', 'senha')

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return user

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == user.username and request.form['password'] == user.password:
            # Usuário autenticado, redireciona para a página inicial
            login_user(user)
            return redirect(url_for('home'))
        else:
            # Credenciais inválidas, exibe mensagem de erro
            error = 'Usuário ou senha incorretos.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
    
    
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
