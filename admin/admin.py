from flask import Blueprint

admins = Blueprint('admin',__name__,template_folder="template",static_folder="static")

@admins.route("/")
def AdminHome():
    return "admin"