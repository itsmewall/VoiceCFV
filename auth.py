from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Definindo um dicionário vazio para armazenar os usuários cadastrados
users = {}

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            error = 'Usuário não existe'
        elif users[username]['password'] != password:
            error = 'Senha incorreta'
        else:
            # Se as credenciais estiverem corretas, redireciona para a página home
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# Rota para a página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username in users:
            error = 'Usuário já existe'
        elif password != confirm_password:
            error = 'Senhas não coincidem'
        else:
            # Adiciona o usuário ao dicionário de usuários
            users[username] = {'password': password}
            # Redireciona para a página de login
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

# Rota para a página home
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
