from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user
from flask_login.utils import login_required

import app as app

admins = Blueprint('admin',__name__,template_folder="template",static_folder="static")

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