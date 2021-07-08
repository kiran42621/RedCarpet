from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.utils import redirect

import app as app

customers = Blueprint('customer',__name__,template_folder="template",static_folder="static")

@customers.route("/<id>")
@login_required
@app.role_required("Customer")
def CustomerHome(id):
    print(type(id))
    print(type(current_user._id))
    if id != str(current_user._id):
        flash("You do not have permission to access this page")
        return redirect(url_for("home"))
    Customer = app.Customers.query.filter_by(_id = id).first()
    Loan = app.Loan.query.filter_by(CustomerID = id).all()
    return render_template("CustomerHome.html", data=Customer, data2=Loan)

