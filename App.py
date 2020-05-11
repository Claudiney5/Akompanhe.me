from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__.split('.')[0])


@app.route('/')
def home():
	return render_template('index.html', component1='active')

@app.route('/kombitas')
def kombitas():
	return render_template('kombitas.html')

@app.route('/cadastro', methods=["POST", "GET"])
def cadastro():
    if request.method == 'POST':
        name = request.form["nm"]
        return redirect(url_for("user", usr=name))
    else:
        return render_template('cadastro.html', component2='active')

@app.route('/<usr>')
def user(usr):
	return f'<h1>{usr}</h1>'

@app.route('/kombits/<profile>')
def kombi_prof():
	return render_template('index.html')

@app.route('/contato')
def contato():
	return render_template('contato.html', component3='active')

@app.route('/links_int')
def links_int():
	return render_template('links_int.html',component4='active')



if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__.split('.')[0])


@app.route('/')
def home():
	return render_template('index.html', component1='active')

@app.route('/kombitas')
def kombitas():
	return render_template('kombitas.html', comp_komb='active')

@app.route('/cadastro', methods=["POST", "GET"])
def cadastro():
    if request.method == 'POST':
        name = request.form["nm"]
        return redirect(url_for("user", usr=name))
    else:
        return render_template('cadastro.html', component2='active')

@app.route('/<usr>')
def user(usr):
	return f'<h1>{usr}</h1>'

@app.route('/kombits/<profile>')
def kombi_prof():
	return render_template('index.html')

@app.route('/contato')
def contato():
	return render_template('contato.html', component3='active')

@app.route('/links_int')
def links_int():
	return render_template('links_int.html',component4='active')



if __name__ == '__main__':
    app.run(debug=True)

