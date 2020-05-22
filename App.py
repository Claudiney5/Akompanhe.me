

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__.split('.')[0])
app.secret_key = "segredo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////kombitas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=30)

db = SQLAlchemy(app)

class KombiHome(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    kombi = db.Column(db.String(25), unique=True, nullable=False)
    propri = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(80), unique=True, nullable=False)
    texto = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, email, kombi, propri, senha, texto):
        self.email = email
        self.kombi = kombi
        self.propri = propri
        self.senha = senha
        self.texto = texto


@app.route('/')
def home():
    return render_template('index.html', component1='active')

@app.route('/kombitas')
def kombitas(): 
    return render_template('kombitas.html', comp_komb='active')

@app.route('/cadastro', methods=["POST", "GET"])
def cadastro():
    email = None
    if request.method == 'POST': 
        session.permanent = False
        propri = request.form['names']
        session["names"] = propri
        email = request.form['new_email']
        session['new_email'] = email
        senha = request.form['new_pass']
        session['new_pass'] = senha
        kombi = request.form['new_kombi']
        session["new_kombi"] = kombi
        texto = request.form['resume']
        session['resume'] = texto

        found_kombi = KombiHome.query.filter_by(email=email).first()
        if found_kombi:
            flash("Este e-mail já esta cadastrado. Faça o seu Login")
            return redirect(url_for('login'))
        else:
            kmb = KombiHome(email, kombi, propri, senha, texto) 
            db.session.add(kmb)
            db.session.commit()

        return redirect(url_for('new'))

    else:
        return render_template('cadastro.html')
    
     
@app.route('/new_profile')
def new():
    if 'new_kombi' in session:
        kombi = session['new_kombi']
        proprietarios = session['names']
        senha = session['new_pass']
        email = session['new_email']
        texto = session['resume']
        return f'''<h1>A  kombita {kombi } pertence a { proprietarios }</h1>
                  Senha : {senha}
                  {texto}'''
                
    else:
        return redirect(url_for('cadastro'))

@app.route('/kombits/<profile>')
def kombi_prof():
    return render_template('index.html')

@app.route('/logout')
def logout():
	session.pop("new_profile", None)
	return redirect(url_for("home"))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/contato')
def contato():
    return render_template('contato.html', component3='active')

@app.route('/links_int')
def links_int():
    return render_template('links_int.html',component4='active')

@app.route('/view')
def view():
    return render_template("view.html", values=KombiHome.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

