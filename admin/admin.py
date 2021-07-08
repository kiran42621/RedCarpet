from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user
from flask_login.utils import login_required
from wtforms import StringField, PasswordField
from flask_wtf import Form
from wtforms.validators import Email, InputRequired, length
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt

import app as app
import bcrypt

admins = Blueprint('admin',__name__,template_folder="template",static_folder="static")

class AddAgent(Form):
    Name = StringField('Name', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Email = StringField('Email', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Password = PasswordField('Password', validators=[InputRequired(message='Required')])

@admins.route("/", methods=['POST','GET'])
@login_required
@app.role_required("Admin")
def AdminHome():
    Loans = app.Loan.query.filter_by().all()
    if request.method == 'POST':
        if request.form.get("Approved"):
            ID = request.form.get("Id")
            Loan = app.Loan.query.filter_by(_id = ID).first()
            Amt = Loan.Amount[len(Loan.Amount)-1]
            Inte = Loan.Interest[len(Loan.Interest)-1]
            Ten = Loan.Tenure[len(Loan.Tenure)-1]
            update_info = app.Loan.query.filter_by(_id = ID).update(dict(Reviewer=current_user.Name,ReviewerID=current_user._id,Status="Approved",RejectMessage="Approved",Amount=Amt,Tenure=Ten,Interest=Inte))
            app.db.session.commit()
            return redirect(url_for("admin.AdminHome"))
        elif request.form.get("Rejected"):
            ID = request.form.get("LoanID")
            Loan = app.Loan.query.filter_by(_id = ID).first()
            msg = Loan.RejectMessage
            msg[len(msg)-1] = request.form.get("RejectMessage")
            update_info = app.Loan.query.filter_by(_id = ID).update(dict(RejectMessage=msg,Status="Rejected"))
            app.db.session.commit()
            return redirect(url_for("admin.AdminHome"))
        else:
            return "error"
    return render_template("AdminHome.html", data = Loans)

@admins.route("/AddAgent", methods=['POST','GET'])
@login_required
@app.role_required("Admin")
def AdminAddAgent():
    AgentAddForm = AddAgent()
    if request.method == 'POST':
        Name = AgentAddForm.Name.data
        Email = AgentAddForm.Email.data
        Password = generate_password_hash(AgentAddForm.Password.data)
        user_found = app.Users.query.filter_by(Email = Email).first()
        if user_found:
            flash("Email already exist try another")
            return render_template("AdminAddAgent.html", form = AgentAddForm)
        else:
            data = app.Users(Name,Email,Password,'Agent')
            app.db.session.add(data)
            app.db.session.commit()
            flash("User Added")
            return render_template("AdminAddAgent.html", form = AgentAddForm)
    return render_template("AdminAddAgent.html", form = AgentAddForm)