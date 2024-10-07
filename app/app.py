from flask import Flask, render_template

app = Flask(__name__)


# @app.route('/')

def index():
    # return "Bienvenido a la pagina de prueba, Hello, World!"
    # return render_template('index.html',titulo='Pagina Principal')
    data={
        'titulo':'Index',
        'encabezado':'Bienvenido(a)'
    }
    return render_template('index.html', data=data)

@app.route('/contacto')
def contacto():
    data={
        'titulo':'Contacto',
        'encabezado':'Bienvenido(a)'
    }
    return render_template('contacto.html', data=data)

@app.route('/holaMundo')
def hola_mundo():
    return "Hola, Mundo"

if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)