from app import app 

from flask import render_template

@app.route("/")
def index():
    return render_template("Index.html")

@app.route("/Jinja")
def Jinja():

    my_name= "stapler"

    return render_template("jinja.html", my_name=my_name)

@app.route("/about")
def about():
    return "<h1 style='color:red'>About!!!!!!</h1>"