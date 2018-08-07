from flask import Flask, render_template, redirect, flash, session, request
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app= Flask(__name__)

app.secret_key="DANKMEMESARENEVERDANKENOUGH"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def submit():
    valid = True
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        valid = False
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        valid = False

    if valid ==False:
        return redirect('/')
    mysql = connectToMySQL('EmailValidation')

    query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, now(), now());"
    
    data = { "email" : request.form['email'] }
    
    email_id = mysql.query_db(query, data)

    return redirect("/success")

@app.route ('/success')
def success():
    mysql = connectToMySQL('EmailValidation')
    all_emails = mysql.query_db("SELECT * FROM emails;")
    return render_template('end.html', emails=all_emails)

@app.route ('/delete/<id>')
def delete(id):
    mysql = connectToMySQL('EmailValidation')
    query = "DELETE from emails where id= %(id)s;"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect("/success")

if __name__=="__main__":
    app.run(debug=True)