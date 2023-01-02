import os
import random
import sqlite3

from flask import Flask, render_template, render_template_string,request,redirect,session
from pymysql import Connect
from flask import session
from pandas import read_table
app = Flask(__name__,static_url_path="/static")
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://'
@app.route("/post", methods=["POST"])
def postentry():
    title = request.form['title']
    content = request.form['description']
    db = Connect(user="aheisleycook",password="A714708o",database="diary")
    conn = db.cursor()
    conn.execute("""insert into ENTRY(ENTRY_ID,ENTRY_TITLE,ENTRY_DESC) values(%s,%s,%s)""",(None,title,content))
    db.commit()
    return redirect("/auth")

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

@app.route("/auth")

def Auth():
    return  render_template("auth.html")

@app.route("/")
def home():
    return redirect("/journal")
@app.route("/journal")
def Landing():
    db = Connect(user="aheisleycook",password="A714708o",database="diary")
    conn = db.cursor()
    conn.execute("select * from ENTRY")
    entries = conn.fetchall()
    return render_template("index.html",entries=entries)

@app.route("/journal/search",methods=["GET"])
def searchbyid():
    title = request.args.get("title")
    def method_name():
        pass
    db = Connect(user="aheisleycook", password="A714708o", database="diary")
    conn = db.cursor()
    conn.execute("select * from ENTRY WHERE ENTRY_TITLE LIKE=%s",title)
    entries = conn.fetchall()
    return render_template("index.html", entries=entries)
@app.route("/login",methods=["post"])
def Login():
    try:
        db = Connect(user="aheisleycook", password="A714708o", database="diary")
        conn = db.cursor()
        username = request.form["username"]
        password = request.form["password"]

        conn.execute(f"select * from USER where USER_NAME='{username}' and USER_PASSWORD='{password}'")

        logon = conn.fetchone()

        if logon:
            session["username"] = logon[1]
            session["password"] = logon[2]

            return  redirect("/journal")
        if not logon:
            return redirect("/auth")
    except sqlite3.OperationalError as error:
        error = error
        return error

app.run(debug=True)
