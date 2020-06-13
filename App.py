

from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__.split('.')[0])
app.secret_key = "segredo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////kombis5.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=30)

db = SQLAlchemy(app)
dropzone = Dropzone(app)

app.config.update(
    #UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_UPLOAD_MULTIPLE = True,
    DROPZONE_PARALLEL_UPLOADS = 12,  # handle 12 file per request
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_DEFAULT_MESSAGE = 'Arraste suas imagens ou cliques aqui para busca-las',
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*',
    DROPZONE_MAX_FILES = 12,
    DROPZONE_MAX_FILE_EXCEED = 'A garagem está cheia. 12 é o número máximo de fotos.'
)


#  Uploads settings
#app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
#photos = UploadSet('photos', IMAGES)
#configure_uploads(app, photos)
#patch_request_class(app)  #  set maximum file size, default is 16MB


class KombiHome(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    kombi = db.Column(db.String(25), unique=False, nullable=False)
    propri = db.Column(db.String(80), unique=False, nullable=False)
    senha = db.Column(db.String(80), unique=False, nullable=False)
    texto = db.Column(db.String(500), unique=False, nullable=False)
    imagens = db.Column(db.LargeBinary)

    def __init__(self, email, kombi, propri, senha, texto, imagens):
        self.email = email
        self.kombi = kombi
        self.propri = propri
        self.senha = senha
        self.texto = texto
        self.imagens = imagens


@app.route('/')
def home():
    return render_template('index.html', component1='active')

@app.route('/kombitas')
def kombitas(): 
    kombi = KombiHome.query.filter_by(kombi='Manjedora').first_or_404()
    return render_template('kombitas.html', comp_komb='active', kombi=kombi)


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

        imagens = request.files

        for key, f in request.files.items():
            if key.startswith('file'):
                imagens.append(f.filename)

        session['imagens'] = imagens

        
        found_kombi = KombiHome.query.filter_by(email=email).first()
        if found_kombi:
            flash("Este e-mail já esta cadastrado. Faça o seu Login")
            return redirect(url_for('login'))
        else:
            kmb = KombiHome(email, kombi, propri, senha, texto, imagens) 
            db.session.add(kmb)
            db.session.commit()

            return redirect(url_for('bemVindo', values=KombiHome.query.all()))

    else:
        
        session.pop('imagens', None)
        return render_template('cadastro.html')



@app.route('/bem-vindo')
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

