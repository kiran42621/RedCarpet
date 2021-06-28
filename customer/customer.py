from flask import Blueprint, render_template, request
from flask_login import current_user

import app as app

customers = Blueprint('customer',__name__,template_folder="template",static_folder="static")

@customers.route("/<id>")
def CustomerHome(id):
    Customer = app.Customers.query.filter_by(_id = id).first()
    Loan = app.Loan.query.filter_by(CustomerID = id).all()
    return render_template("CustomerHome.html", data=Customer, data2=Loan)

