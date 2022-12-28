from flask import Flask, render_template, render_template_string,request,redirect
from pymysql import Connect
app = Flask(__name__,static_url_path="/static")

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

@app.route("/journal/<id>")
def searchbyid(id):
    db = Connect(user="aheisleycook", password="A714708o", database="diary")
    conn = db.cursor()
    conn.execute("select * from ENTRY WHERE ENTRY_ID={0}",id)
    entries = conn.fetchall()
    return render_template("index.html", entries=entries)
app.run()