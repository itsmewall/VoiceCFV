from flask import Flask, g, render_template, redirect, url_for, request, jsonify
import sqlite3
from werkzeug.local import LocalProxy

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'PRIVATE'

# Criando a conexão com o banco de dados para cada thread
def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect('users.db')
    return g.db

# Fechando a conexão do banco de dados quando o aplicativo é encerrado
@app.teardown_appcontext
def close_db(error):
    if hasattr(app, 'db'):
        app.db.close()

# Definindo um dicionário vazio para armazenar os usuários cadastrados
users = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Obtendo a conexão do banco de dados para este thread
        db = get_db()
        cur = db.cursor()
        # Executando a consulta para verificar se o usuário existe
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if not row:
            error = 'Usuário não existe'
        elif row[1] != password:
            error = 'Senha incorreta'
        else:
            # Se as credenciais estiverem corretas, redireciona para a página home
            return redirect(url_for('home', username=username))
    return render_template('login.html', error=error)

# Rota para a página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Obtendo a conexão do banco de dados para este thread
        db = get_db()
        cur = db.cursor()
        # Executando a consulta para verificar se o usuário já existe
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            error = 'Usuário já existe'
        elif password != confirm_password:
            error = 'Senhas não coincidem'
        else:
            # Adicionando o novo usuário ao banco de dados
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            # Redirecionando para a página de login
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

# Rota para a página home
@app.route('/home')
def home():
    username = request.args.get('username')
    return render_template('home.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
