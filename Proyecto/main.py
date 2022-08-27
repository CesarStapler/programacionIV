from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import requests


app = Flask(__name__)
api = Api(app)


class Citas(Resource):
    def get(self):
        data = pd.read_csv('citas.csv')
        data = data.to_dict()
        return {'citas': data}, 200

    def post(self):
        print("entre")
        parser = reqparse.RequestParser()

        parser.add_argument('Id', type=str, required=True)
        parser.add_argument('Apellido', type=str, required=True)
        parser.add_argument('Nombre', type=str, required=True)
        parser.add_argument('Cedula', type=str, required=True)
        parser.add_argument('Fecha', type=str, required=True)
        parser.add_argument('Tel', type=str, required=True)
        parser.add_argument('Estado', type=str, required=True)

        args = parser.parse_args()
        print(args['Id'])
        new_data = pd.DataFrame({
            'Id': [args['Id']],
            'Apellido': [args['Apellido']],
            'Nombre': [args['Nombre']],
            'Cedula': [args['Cedula']],
            'Tel': [args['Tel']],
            'Fecha': [args['Fecha']],
            'Estado': [args['estado']],
        })

        data = pd.read_csv('citas.csv')
        data = data.append(new_data, ignore_index=True)
        data.to_csv('citas.csv', index=False)
        return {'data': data.to_dict()}, 200


    pass


api.add_resource(Citas, '/citas')




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        users = requests.get("http://127.0.0.1:5000/citas").json()
        id = len(users['citas']['Id']) + 1
        apellido = request.form['apellido']
        nombre = request.form['nombre'
        cedula = request.form['cedula']
        tel = request.form['tel']
        fecha = request.form['fecha']
        estado = request.form['Estado']

        requests.post("http://127.0.0.1:5000/citas", params={
                      'Id': id, 'Apellido': apellido,'Nombre': nombre, 'Cedula': cedula, 'Tel': tel, 'Fecha': fecha,  'estado': estado})
        return render_template("index.html")

    return render_template("index.html")


@app.route('/mostrar_citas', methods=['GET', 'POST'])
def mostrarcitas():
    users = requests.get("http://127.0.0.1:5000/citas").json()
    nombres = users['citas']['Nombre']
    for nombre in nombres:
        print(nombres[nombre])

    return render_template("mostrar_citas",apellidos=users['citas']['Apellido'], nombres=users['citas']['Nombre'],  cedulas=users['citas']['Cedula'], tel=users['citas']['Telefono'], fechas=users['citas']['Fecha'], estado=users['estado']['estado'])


if __name__ == '__main__':
    app.run()