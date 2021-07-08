import bcrypt

from datetime import datetime
from flask import Blueprint, render_template, request, flash
from flask.helpers import flash, url_for
from flask_login.utils import login_required
from flask_wtf import FlaskForm, Form
from sqlalchemy.sql.expression import update
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SelectField, form
from wtforms.fields.core import IntegerField
from wtforms.validators import Email, InputRequired, length
from flask_login import current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import insert

import app as app

agents = Blueprint('agent',__name__,template_folder="template",static_folder="static")

class AddCustomer(Form):
    Name = StringField('Name', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Email = StringField('Email', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Password = PasswordField('Password', validators=[InputRequired(message='Required')])
    Address = StringField('Address', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Salary = IntegerField('Salary', validators=[InputRequired(message='Required')])

@agents.route("/AgentHome")
@login_required
@app.role_required("Agent")
def AgentHome():
    try:
        Customer = app.Customers.query.filter_by(AgentID = current_user._id).all()
        Loan = app.Loan.query.filter_by(AgentID = current_user._id).all()
    except:
        pass
    return render_template("AgentHome.html", data=Customer, data2=Loan)

@agents.route("/AgentViewCustomer/<id>", methods=['POST','GET'])
@login_required
@app.role_required("Agent")
def AgentViewCustomer(id):
    Customer = app.Customers.query.filter_by(_id = id).first()
    if request.method == 'POST':
        if request.form.get("Update"):
            ID = request.form.get("id")
            Name = request.form.get("Name")
            Email = request.form.get("Email")
            Address = request.form.get("Address")
            Salary = request.form.get("Salary")
            User = app.Customers.query.filter(Email == Email, id != ID).all()
            if User:
                flash("Email Already Choosen")
                return redirect("agent/AgentViewCustomer/{}".format(ID))
            else:
                Change = app.Customers.query.filter_by(_id = ID).first()
                Change.Name = Name
                Change.Email = Email
                Change.Address = Address
                Change.Salary = Salary
                app.db.session.commit()
                flash("Done")
                return redirect(url_for("agent.AgentViewCustomer",id=ID))
        elif request.form.get("Apply"):
            ID = request.form.get("id")
            Name = request.form.get("Name")
            Email = request.form.get("Email")
            Address = request.form.get("Address")
            Salary = request.form.get("Salary")
            AgentID = current_user._id
            AgentName = current_user.Name
            Dates = datetime.now().strftime('%Y-%m-%d')
            Amount = []
            Amount.append(request.form.get("hiddenAmount"))
            Interest = []
            Interest.append(request.form.get("hiddenInterest"))
            Tenure = []
            Tenure.append(request.form.get("hiddenTenure"))
            Status = "New"
            RejectMsg = []
            RejectMsg.append("")
            Loan = app.Loan(AgentID,AgentName,ID,Name,Dates,Email,Address,Salary,Amount,Interest,Tenure,Status,'',0,RejectMsg)
            app.db.session.add(Loan)
            app.db.session.commit()
            flash("Loan Requested")
            return render_template("AgentViewCustomer.html", data = Customer)
    return render_template("AgentViewCustomer.html", data = Customer)

@agents.route("/AgentViewLoan/<id>", methods=['POST','GET'])
@login_required
@app.role_required("Agent")
def AgentViewLoan(id):
    Loan = app.Loan.query.filter_by(_id = id).first()
    if Loan.Status == "Approved":
        flash("Loan Already Approved cannot modify")
        return redirect(url_for("agent.AgentHome"))
    if request.method == 'POST':
        ID = request.form.get("id")
        Interest = request.form.get("hiddenInterest")
        Amount = request.form.get("hiddenAmount")
        Tenure = request.form.get("hiddenTenure")
        Sel_Loan = app.Loan.query.filter_by(_id = ID).first()
        # Sel_Loan.Amount= Sel_Loan.Amount.append(Amount)
        Amt = Sel_Loan.Amount
        Inte = Sel_Loan.Interest
        Ten = Sel_Loan.Tenure
        Amt.append(Amount)
        Inte.append(Interest)
        Ten.append(Tenure)
        update_info = app.Loan.query.filter_by(_id = ID).update(dict(Amount=Amt,Interest=Inte,Tenure=Ten,Status="Modified"))
        app.db.session.commit()
        return redirect(url_for("agent.AgentViewLoan",id = ID))
    return render_template("AgentViewLoan.html", data = Loan)

@agents.route("/AgentAddCustomer", methods=['POST','GET'])
@login_required
@app.role_required("Agent")
def AgentAddCustomer():
    CustomerAddForm = AddCustomer()
    if request.method == 'POST':
        Name = CustomerAddForm.Name.data
        Email = CustomerAddForm.Email.data
        Password = generate_password_hash(CustomerAddForm.Password.data)
        Address = CustomerAddForm.Address.data
        Salary = CustomerAddForm.Salary.data
        AgentID = current_user._id
        user_found = app.Customers.query.filter_by(Email = Email).first()
        if user_found:
            flash("Email already exist try another")
            return render_template("AgentAddCustomer.html", form = CustomerAddForm)
        else:
            data = app.Customers(Name,Email,Password,Address,Salary,AgentID,'Customer')
            app.db.session.add(data)
            app.db.session.commit()
            flash("User Added")
            return render_template("AgentAddCustomer.html", form = CustomerAddForm)
    return render_template("AgentAddCustomer.html", form = CustomerAddForm)