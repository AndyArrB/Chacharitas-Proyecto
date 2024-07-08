from flask import render_template, url_for, request, redirect, jsonify

from app import app

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/shop-single")
def shop_single():
    return render_template("shop-single.html")


@app.route("/dios")
def dios():
    return render_template("logins.html")
