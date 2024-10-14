from flask import Flask, render_template, request, redirect, session, flash, url_for


# flask==2.0.2

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario('teste', 'teste', '1234')
usuario2 = Usuario('pedrrin', 'ph', 'pedro1234')
usuario3 = Usuario('fael', 'chefe', 'fael1234')

usuarios = {usuario1.nickname: usuario1,
            usuario2.nickname: usuario2,
            usuario3.nickname: usuario3}

jogo1 = Jogo('Pokemon', 'JRPG', 'Switch')
jogo2 = Jogo('Valorant', 'FPS', 'PC')
jogo3 = Jogo('Stardew', 'Farm', 'PC')
lista_jogos = [jogo1, jogo2, jogo3]

app = Flask(__name__)
app.secret_key = 'cuzin'


@app.route('/')
def index():  # put application's code here

    return render_template('index.html', titulo='Jogos', jogos=lista_jogos)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    new_jogo = Jogo(nome, categoria, console)
    lista_jogos.append(new_jogo)

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    nickname = request.form['usuario']
    if nickname in usuarios:
        usuario = usuarios[nickname]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname

            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuario não logado')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout com sucesso!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
