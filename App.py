

from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
import sys
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, validators, PasswordField
from werkzeug.utils import secure_filename
import flask_heroku
flask_heroku.settings(locals())

basedir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__.split('.')[0])
app.secret_key = "segredo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////kombis4.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=30)

db = SQLAlchemy(app)
dropzone = Dropzone(app)

app.config.update(
    DROPZONE_UPLOAD_MULTIPLE = True,
    DROPZONE_PARALLEL_UPLOADS = 12,  # handle 12 file per request
    UPLOADED_PATH=os.path.join(basedir, 'kombits'),
    DROPZONE_DEFAULT_MESSAGE = "Arraste suas imagens ou cliques aqui para busca-las",
    DROPZONE_ALLOWED_FILE_TYPE = 'image',
    DROPZONE_MAX_FILES = 12,
    DROPZONE_MAX_FILE_EXCEED = 'A garagem está cheia. 12 é o número máximo de fotos.',
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_REDIRECT_VIEW='bemVindo'
)


class KombiHome(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    kombi = db.Column(db.String(25), unique=False, nullable=False)
    propri = db.Column(db.String(80), unique=False, nullable=False)
    senha = db.Column(db.String(80), unique=False, nullable=False)
    texto = db.Column(db.String(500), unique=False, nullable=False)

    def __init__(self, email, kombi, propri, senha, texto):
        self.email = email
        self.kombi = kombi
        self.propri = propri
        self.senha = senha
        self.texto = texto



class RegistrationForm(Form):
    propri = StringField('nomes', [validators.Length(min=2, max=25)])
    email = StringField('new_email', [
        validators.Length(min=6, message=(u'Muito pequeno para um endereço de email, não?')),
        validators.Email(message=(u'Não é um email válido!'))
    ])
    senha = PasswordField('new_pass', [validators.DataRequired()])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html', component1='active')

@app.route('/kombitas')
def kombitas(): 
    # for i in range(6):
    #     kombi[i] = KombiHome.query.filter_by(kombi=i).first_or_404()
    return render_template('kombitas.html', comp_komb='active')


@app.route('/cadastro', methods=["POST", "GET"])
def cadastro():
    email = None
   
    if request.method == 'POST' : 
        session.permanent = False

        propri = request.form.get('nomes')
        session['nomes'] = propri
        email = request.form.get('new_email')
        session['new_email'] = email
        senha = request.form.get('new_pass')
        session['new_pass'] = senha
        kombi = request.form.get('new_kombi')
        session["new_kombi"] = kombi
        texto = request.form.get('resume')
        session['resume'] = texto
        
        found_kombi = KombiHome.query.filter_by(email=email).first()
        if found_kombi:
            flash("Este e-mail já esta cadastrado. Faça o seu Login")
            return redirect(url_for('login'))
        else:
            kmb = KombiHome(email, kombi, propri, senha, texto) 

            db.session.add(kmb)
            db.session.commit()

            return render_template('fotos.html', kmb=kmb)

    else:
        
        session.pop('imagens', None)
        return render_template('cadastro.html')


@app.route('/fotos', methods=['POST', 'GET'])
def fotos():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('bem-vindo.html')

@app.route('/bem-vindo', methods=['POST', 'GET'])
def bemVindo():
    return render_template('bem-vindo.html')
    
     
@app.route('/new_profile')
def new():
    if request.method == 'POST':
        kombi = session['new_kombi']
        propri = session['names']
        senha = session['new_pass']
        email = session['new_email']
        texto = session['resume']

        return render_template('index.html')
                
    else:
        return render_template('new.html')

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
    if request.method == 'POST': 
        session.permanent = False
        email = request.form['email']
        session['email'] = email
        senha = request.form['senha']
        session['senha'] = senha
        return redirect(url_for('kombi_prof'))
    else:
        return render_template("view.html", values=KombiHome.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

