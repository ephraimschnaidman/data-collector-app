from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/bmi_collector'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    weight_=db.Column(db.Float)
    height_=db.Column(db.Float)
    bmi_=db.Column(db.Float)

    def __init__(self, email_, weight_, height_, bmi_):
        self.email_=email_
        self.weight_=weight_
        self.height_=height_
        self.bmi_=bmi_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        weight=float(request.form["weight_num"])
        height=float(request.form["height_num"])
        bmi=float(weight/(height*height))
        bmi=round(bmi,2)
        # BMI = weight (kg) ÷ height2 (m2)

        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data=Data(email,weight,height,bmi)
            db.session.add(data)
            db.session.commit()
            avg_bmi=db.session.query(func.avg(Data.bmi_)).scalar()
            avg_bmi=round(avg_bmi,2)
            count=db.session.query(Data.bmi_).count()
            send_email(email, weight, height, bmi, avg_bmi, count)
            return render_template("success.html")
    return render_template("index.html",
    text="Note: Email already in database.")

if __name__== '__main__':
    app.debug=True
    app.run(port=5001)
