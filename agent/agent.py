from datetime import datetime
from flask import Blueprint, render_template, request
from flask.helpers import flash, url_for
from flask_wtf import FlaskForm, Form
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SelectField, form
from wtforms.fields.core import IntegerField
from wtforms.validators import Email, InputRequired, length
from flask_login import current_user

import app as app

agents = Blueprint('agent',__name__,template_folder="template",static_folder="static")

class AddCustomer(Form):
    Name = StringField('Name', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Email = StringField('Email', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Password = PasswordField('Password', validators=[InputRequired(message='Required')])
    Address = StringField('Address', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Salary = IntegerField('Salary', validators=[InputRequired(message='Required')])

@agents.route("/AgentHome")
def AgentHome():
    Customer = app.Customers.query.filter_by(AgentID = current_user._id).all()
    return render_template("AgentHome.html", data=Customer)

@agents.route("/AgentViewCustomer/<id>", methods=['POST','GET'])
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
            Amount = request.form.get("AmountRange")
            Interest = request.form.get("InterestRange")
            Tenure = request.form.get("TenureRange")
            Status = "New"
            # print(Interest +"_"+ Tenure +"_"+ Amount)
            print(ID)
            print(Interest)
            return "Button Apply"
    return render_template("AgentViewCustomer.html", data = Customer)

@agents.route("/AgentAddCustomer", methods=['POST','GET'])
def AgentAddCustomer():
    CustomerAddForm = AddCustomer()
    if request.method == 'POST':
        Name = CustomerAddForm.Name.data
        Email = CustomerAddForm.Email.data
        Password = CustomerAddForm.Password.data
        Address = CustomerAddForm.Address.data
        Salary = CustomerAddForm.Salary.data
        AgentID = current_user._id
        user_found = app.Customers.query.filter_by(Email = Email).first()
        if user_found:
            flash("Email already exist try another")
            return render_template("AgentAddCustomer.html", form = CustomerAddForm)
        else:
            data = app.Customers(Name,Email,Password,Address,Salary,AgentID)
            app.db.session.add(data)
            app.db.session.commit()
            flash("User Added")
            return render_template("AgentAddCustomer.html", form = CustomerAddForm)
    return render_template("AgentAddCustomer.html", form = CustomerAddForm)