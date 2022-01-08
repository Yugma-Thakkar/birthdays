import os
import re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

operations = []

@app.route("/", methods=["GET"])
def index():

    birthdays = db.execute("SELECT * FROM birthdays")

    if request.args.get("response") == "json":
        return jsonify(operations)
    else:
        return render_template("index.html", birthdays = birthdays)

@app.route("/insert", methods=["POST"])
def insert():
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")
    
    db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name.strip(), month, day)

    operations.append({
        "op": "insert",
        "name": name,
        "month": month,
        "day": day
    })

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    print("HI BRO", request.args)
    if request.method == "POST":
        delete = request.args.get("username")
        print(f"DELETE FROM birthdays WHERE name = '{delete}'")

        db.execute("DELETE FROM birthdays WHERE name = ?", delete)

        operations.append({
            "op": "delete",
            "name": delete,
        })

        return "ok"

@app.route("/edit", methods=["POST"])
def edit():
    bday = request.args.get("bday")
    month, day = bday.split("/")
    
    name = request.args.get("name")
    db.execute("UPDATE birthdays SET month = ?, day = ? WHERE name = ?", month, day, name)

    operations.append({
        "op": "edit",
        "name": name,
        "month": month,
        "day": day
    })

    return "ok"


#test
