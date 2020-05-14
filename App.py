

from flask import Flask, redirect, url_for, render_template, request,session


app = Flask(__name__.split('.')[0])
app.secret_key = "segredo"


@app.route('/')
def home():
    return render_template('index.html', component1='active')

@app.route('/kombitas')
def kombitas():
    return render_template('kombitas.html', comp_komb='active')

@app.route('/cadastro', methods=["POST", "GET"])
def cadastro():
    if request.method == 'POST':
        session["names"] = request.form['names']
        session['new_email'] = request.form['new_email']
        session['new_pass'] = request.form['new_pass']
        session["new_kombi"] = request.form['new_kombi']
        session['resume'] = request.form['resume']
        return redirect(url_for("new"))
    else:
        return render_template('cadastro.html', component2='active')
      
@app.route('/new_profile')
def new():
    if 'new_kombi' in session:
        kombi = session['new_kombi']
        proprietarios = session['names']
        senha = session['new_pass']
        email = session['new_email']
        texto = session['resume']
        return f'''<h1>A  kombita { kombi } pertence a { proprietarios }</h1>
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

@app.route('/contato')
def contato():
    return render_template('contato.html', component3='active')

@app.route('/links_int')
def links_int():
    return render_template('links_int.html',component4='active')


if __name__ == '__main__':
    app.run(debug=True)

