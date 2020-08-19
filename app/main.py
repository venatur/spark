from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "payments.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)


@app.route('/', methods=["GET", "POST"])
def home():
    bills = None
    if request.form:
        try:
            pay = Payment(name_payment=request.form.get("name_payment"), import_payment=request.form.get("import_payment"))
            db.session.add(pay)
            db.session.commit()
        except Exception as e:
            print("falla al escribir en db")
            print(e)
    bills = Payment.query.all()
    return render_template('index.html', bills=bills)


@app.route("/update", methods=["POST"])
def update():
    newimport = request.form.get("newimport1")
    oldimport = request.form.get("oldimport1")
    newimport2 = request.form.get("newimport2")
    pay = Payment.query.filter_by(name_payment=oldimport).first()
    pay.name_payment = newimport
    pay.import_payment = newimport2
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    name_payment = request.form.get("name_payment")
    pay = Payment.query.filter_by(name_payment=name_payment).first()
    db.session.delete(pay)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
