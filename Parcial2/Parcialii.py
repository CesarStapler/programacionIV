from flask import Flask, render_template
from flask_restful import Resource, Api
import pandas as pd
import requests
import decimal


app = Flask(__name__)
api = Api(app)


class Vacunas(Resource):
    def get(self):
        data = pd.read_csv('worldbankDB.csv',
                           error_bad_lines=False, engine='python')
        data = data.to_dict()
        return {'data': data}, 200

pass 

api.add_resource(Vacunas, '/vacunas')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datosvacunas')
def datosvacunas():
    data = requests.get('http://127.0.0.1:5000/vacunas').json()
    countryname = (data['data']['Data Source'].get("2"))
    totalData = len(data['data'])
    i = 0
    percentafter = 0 
    year = 0
    for db in data['data']:
        i += 1
        actual = db
        if (totalData - 1 == i):
            percentafter = data["data"][actual]["2"]
            year = actual 

    return render_template('datosvacunas.html', pais=countryname, percentdata=percentafter, year=year)


@app.route('/disponibilidad')
def disponibilidad():
    data = requests.get('http://http://127.0.0.1:5000/vacunas').json()
    totalData = len(data['data'])
    i = 0
    percentdata = 0
    for db in data['data']:
        i += 1
        actual = db
        if(1 > 4):
            percentdata += data["data"][actual]["2"]
            percent = decimal.Decimal(percentdata/(totalData - 4))
            print(int(totalData))

    return  render_template('disponibilidad.html', percent=round(percent, 2))

if __name__ == '__main__':
    app.run()