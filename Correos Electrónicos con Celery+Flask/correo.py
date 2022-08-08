from flask import Flask, render_template, request
from flask_mail import Mail, Message
from celery import Celery


import redis
PalClave = "clave"
DefinicionClave = "definicion"

r = redis.Redis(host='127.0.0.1', port=6379)
r.set("id", -1)


def comprobarPalabra(clave):
    CantPalabras = r.llen(PalClave)
    PalabraExistente = False
    for i in range(CantPalabras):
        PalabraActual = r.lindex(PalClave, i).decode('utf-8')
        if(PalabraActual == clave):
            PalabraExistente = True
            break
    return PalabraExistente


def nuevaPalabra(clave, definicion):
    r.incr("id")
    r.rpush(PalClave, clave)
    r.rpush(DefinicionClave, definicion)
    print("\n palabra agregada correctamente!")


def Actualizar(NvoPalabra, AntPalabra, NvaDefinicion):
    CantPalabras = r.llen(PalClave)
    for i in range(CantPalabras):
        PalabraActual = r.lindex(PalClave, i).decode('utf-8')
        if(PalabraActual == AntPalabra):
            r.lset(PalClave, i, NvoPalabra)
            r.lset(DefinicionClave, i, NvaDefinicion)
            break

    print("\n !Fue" + AntPalabra + "actualizada!")


def EliminarPalabra(clave):
    CantPalabras = r.llen(PalClave)
    for i in range(CantPalabras):
        PalabraActual = r.lindex(PalClave, i).decode('utf-8')
        DefinicionActual = r.lindex(DefinicionClave, i).decode('utf-8')
        if(PalabraActual == clave):
            r.lrem(PalClave, i, PalabraActual)
            r.lrem(DefinicionClave, i, DefinicionActual)
            break
    print("\n ¡Palabra eliminada!")


def ShowAllWords():
    CantPalabras = r.llen(PalClave)
    palabras = []

    for i in range(CantPalabras):
        palabras.append({"name": r.lindex(PalClave, i).decode(
            "utf-8"), "definicion": r.lindex(DefinicionClave, i).decode("utf-8")})
    return palabras


print(r.keys())

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template("Index.html")


@app.route('/AgregarPalabra', methods=['GET', 'POST'])
def AgregarPalabra():
    if request.method == 'POST':
        clave = request.form["word"]
        definicion = request.form["meaning"]
        if comprobarPalabra(clave) == False:
            nuevaPalabra(clave, definicion)
            return render_template("AgregarPalabra.html", message="!!Palabra añadida :)")
        else:
            return render_template("AgregarPalabra.html", message="!!La palabra ya existe :(")

    return render_template("AgregarPalabra.html")


@app.route('/EditarPalabra', methods=['GET', 'POST'])
def EditarPalabra():
    if request.method == 'POST':
        AntiguaPalabra = request.form["oldWord"]
        NuevaPalabra = request.form["word"]
        NuevaDefinicion = request.form["meaning"]

        if comprobarPalabra(AntiguaPalabra):
            Actualizar(AntiguaPalabra, NuevaPalabra, NuevaDefinicion)

            return render_template("EditarPalabra.html", message=False)
        else:

            return render_template("EditarPalabra.html", message=True)

    return render_template("EditarPalabra.html")


@app.route('/EliminarPalabra', methods=['GET', 'POST'])
def eliminarPalabra():
    if request.method == 'POST':
        clave = request.form["word"]

        if comprobarPalabra(clave):
            EliminarPalabra(clave)
            ShowAllWords()
            return render_template("EliminarPalabra.html", message=False)
        else:
            ShowAllWords()
            return render_template("EliminarPalabra.html", message=True)

    return render_template("EliminarPalabra.html")


@app.route('/ListadoPalabras', methods=['GET', 'POST'])
def listadoPalabra():
    allPalabras = ShowAllWords()

    return render_template("ListadoPalabras.html", palabras=allPalabras)


@app.route('/BuscarSignificado', methods=['GET', 'POST'])
def BuscarSignificado():
    if request.method == 'POST':
        clave = request.form["palabra"]
        if comprobarPalabra(clave):
            CantPalabras = r.llen(PalClave)
            for i in range(CantPalabras):
                PalabraActual = r.lindex(PalClave, i).decode('utf-8')
                if(PalabraActual == clave):
                    getPalabra = {"palabra": clave, "definicion": r.lindex(
                        DefinicionClave, i).decode("utf-8")}

                    return render_template("BuscarSignificado.html", ShowWord=getPalabra)
        else:
            return render_template("BuscarSignificado.html", message=True)
    return render_template("BuscarSignificado.html")

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '57f2ff6b9a0188'
app.config['MAIL_PASSWORD'] = 'f82835a15c4057'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

celery = Celery(app.name, broker='redis://localhost:6379/0')
mail = Mail(app)


@Celery.task
def send_async_email(email_data):
    print(email_data + "hola")
    msg = Message(email_data['subject'],
                  sender='aldes@quintero.com',
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    mail.send(msg)

@app.route('/sendEmail', methods=['GET', 'POST'])
def sendEmail():
    if request.method == 'GET':
        return render_template('sendEmail.html')

    email = request.form['email']
    message = request.form['message']

    email_data = {
        'subject': 'Hello from the other side!',
        'to': email,
        'body': message,
    }

    send_async_email(email_data)


if __name__ == "__main__":
    app.run(debug=True)  

