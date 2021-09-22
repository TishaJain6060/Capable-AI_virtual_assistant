import os
from flask import Flask, render_template, request, redirect, url_for, session, Response, flash, jsonify
from difflib import SequenceMatcher
from werkzeug.utils import secure_filename
import func as function
import requests

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def homepage():
   if request.method=='GET':
      value = request.form.get('btn')
      file= open('func.py', 'r').read()
   
   return render_template('homepage.html')

@app.route("/main", methods=["POST", "GET"])
def main():
    return render_template('main.html')

@app.route("/menu", methods=["POST", "GET"])
def menu():
    return render_template('menu.html')

@app.route("/about", methods=["POST", "GET"])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run( debug=True)
