from flask import Blueprint, render_template, redirect, request

admins = Blueprint('admin',__name__,template_folder="template",static_folder="static")

@admins.route("/", methods=['GET','POST'])
def AdminHome():
    if request.method == 'POST':
        print("Hello")
        if request.form.get("Approved"):
            return "Approved"
        elif request.form.get("Rejected"):
            return "Rejected"
    return render_template("AdminHome.html")