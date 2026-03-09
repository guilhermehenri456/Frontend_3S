from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import db_session, Funcionario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vanessa'

login_manager = LoginManager(app)
login_manager.login_message = 'login'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    user = select(Funcionario).where(Funcionario.id == int(user_id))
    resultado = db_session.execute(user).scalar_one_or_none()
    return resultado


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Pega o campo do formulario [lista de campos]
        email = request.form['form-email']
        senha = request.form['form-senha']

        if not email or not senha:
            flash("preencha todos os campos", "alert-danger")
            return render_template("login.html")
        else:
            email_sql = select(Funcionario).where(Funcionario.email == email)
            resultado_email = db_session.execute(email_sql).scalar_one_or_none()

            if resultado_email:
                resultado_email.check_password(senha)
                # Realiza a autenticação
                login_user(resultado_email)
                flash("Login realizado com sucesso", "alert-success")
                return redirect(url_for("home"))

            else:
                flash("Email incorreto", "alert-danger")
                return redirect(url_for("login"))
    return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_funcionario():
    if request.method == 'POST':
        nome = request.form.get('form-nome')
        data_nascimento = datetime.strptime(request.form['form-data_nascimento'], '%Y-%m-%d')
        cpf = request.form.get('form-cpf')
        email = request.form.get('form-email')
        senha = request.form.get('form-senha')
        cargo = request.form.get('form-cargo')
        salario = float(request.form.get('form-salario'))

        if not nome or not email or not senha or not data_nascimento or not cpf or not cargo or not salario:
            flash(f'Preencher todos os campos', 'danger')
            return redirect(url_for('login'))

        verifica_email = select(Funcionario).where(Funcionario.email == email)
        verifica_cpf = select(Funcionario).where(Funcionario.cpf == cpf)
        existe_email = db_session.execute(verifica_email, ).scalar_one_or_none()
        existe_cpf = db_session.execute(verifica_cpf, ).scalar_one_or_none()
        if existe_email:
            flash(f'Email {email} ja existente', 'danger')
            return render_template('funcionarios.html')
        if existe_cpf:
            flash(f'CPF {cpf} ja existente ', 'danger')
            return render_template('funcionarios.html')
        try:
            novo_usuario = Funcionario(nome=nome, data_nascimento=data_nascimento, cpf=cpf, email=email, cargo=cargo,
                                       salario=float(salario))
            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash(f'Funcionario {nome} cadastrado com sucesso', 'success')
            return redirect(url_for('funcionarios'))
        except SQLAlchemyError as e:
            flash(f'Erro na base de dados ao cadastrar funcionario', 'danger')
            print(f'Error na base de dados: {e}')
            return render_template('funcionarios.html')
        except Exception as e:
            flash(f'Erro ao cadastrar funcionario', 'danger')
            print(f'Error ao cadastrar: {e}')
            return redirect(url_for('funcionarios'))
    return render_template('funcionarios.html')


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/calculos')
def calculos():
    return render_template("calculos.html")


@app.route('/funcionarios')
@login_required
def funcionarios():
    funcionarios_sql = select(Funcionario)
    resultado = db_session.execute(funcionarios_sql).scalars().all()
    return render_template("funcionarios.html", resultado=resultado)


@app.route('/geometria')
def geometria():
    return render_template("geometria.html")


@app.route('/operacoes')
def operacoes():
    return render_template("operacoes.html")


@app.route('/somar', methods=['GET', 'POST'])
def somar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            soma = n1 + n2
            flash("deu certo", "alert-success")
            return render_template("operacoes.html", n1=n1, n2=n2, soma=soma)
        else:
            # Passo 1: Emitir a mensagem e a categoria do flash
            flash("preencha o campo vazio", "alert-danger")
    return render_template("operacoes.html")


@app.route('/subtrair', methods=['GET', 'POST'])
def subtrair():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            subtrair = n1 - n2
            return render_template("operacoes.html", n1=n1, n2=n2, subtrair=subtrair)


@app.route('/divisao', methods=['GET', 'POST'])
def divisao():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            divisao = n1 / n2
            return render_template("operacoes.html", n1=n1, n2=n2, divisao=divisao)


@app.route('/multiplicar', methods=['GET', 'POST'])
def multiplicar():
    if request.method == 'POST':
        if request.form['form-n1'] and request.form['form-n2']:
            n1 = int(request.form['form-n1'])
            n2 = int(request.form['form-n2'])
            multiplicar = n1 * n2
            return render_template("operacoes.html", n1=n1, n2=n2, multiplicar=multiplicar)


@app.route('/p_triangulo', methods=['GET', 'POST'])
def p_triangulo():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            p_triangulo = n1 * 3
            return render_template("geometria.html", n1=n1, p_triangulo=p_triangulo)


@app.route('/a_triangulo', methods=['GET', 'POST'])
def a_triangulo():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            a_triangulo = (n1 * 1.732) / 4
            return render_template("geometria.html", n1=n1, a_triangulo=a_triangulo)


@app.route('/p_quadrado', methods=['GET', 'POST'])
def p_quadrado():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            p_quadrado = n1 * 4
            return render_template("geometria.html", n1=n1, p_quadrado=p_quadrado)


@app.route('/a_quadrado', methods=['GET', 'POST'])
def a_quadrado():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            a_quadrado = n1 * n1
            return render_template("geometria.html", n1=n1, a_quadrado=a_quadrado)


@app.route('/p_circulo', methods=['GET', 'POST'])
def p_circulo():
    if request.method == 'POST':
        if request.form['form-r1']:
            r1 = int(request.form['form-r1'])
            p_circulo = 2 * 3.14 * r1
            return render_template("geometria.html", r1=r1, p_circulo=p_circulo)


@app.route('/a_circulo', methods=['GET', 'POST'])
def a_circulo():
    if request.method == 'POST':
        if request.form['form-r1']:
            r1 = int(request.form['form-r1'])
            a_circulo = 3.14 * (r1 * r1)
            return render_template("geometria.html", r1=r1, a_circulo=a_circulo)


@app.route('/p_hexagono', methods=['GET', 'POST'])
def p_hexagono():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            p_hexagono = n1 * 6
            return render_template("geometria.html", n1=n1, p_hexagono=p_hexagono)


@app.route('/a_hexagono', methods=['GET', 'POST'])
def a_hexagono():
    if request.method == 'POST':
        if request.form['form-n1']:
            n1 = int(request.form['form-n1'])
            a_hexagono = ((n1 * n1) * (3 * 1.732)) / 2
            return render_template("geometria.html", n1=n1, a_hexagono=a_hexagono)


# TODO Final do código

if __name__ == '__main__':
    app.run(debug=True, port=5005)
