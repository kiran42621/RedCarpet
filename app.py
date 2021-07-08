import os

from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, InputRequired, length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
from flask_abort import abort
from flask_bcrypt import Bcrypt

try:
    from admin.admin import admins
    from agent.agent import agents
    from customer.customer import customers

except:
    pass

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'RedCarpet.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Kcube"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

UserTypes = {'Agent':'Agent','Admin':'Admin','Customer':'Customer'}


class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    _id = db.Column("id", db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Role = db.Column(db.String(255))

    def __init__(self, Name, Email, Password, Role):
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.Role = Role

    def get_id(self):
        return (self._id)

    def get_role(self):
        return (self.Role)

class Customers(UserMixin, db.Model):
    __tablename__ = 'Customers'
    _id = db.Column("id", db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Password = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    Salary = db.Column(db.Integer)
    AgentID = db.Column(db.Integer)
    Role = db.Column(db.String(255))

    def __init__(self, Name, Email, Password, Address, Salary, AgentID, Role):
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.Address = Address
        self.Salary = Salary
        self.AgentID = AgentID
        self.Role = Role

    def get_id(self):
        return (self._id)

    def get_role(self):
        return (self.Role)

class Loan(db.Model):
    __tablename__ = 'Loan'
    _id = db.Column("id", db.Integer, primary_key=True)
    AgentID = db.Column(db.Integer)
    AgentName = db.Column(db.String(255))
    CustomerID = db.Column(db.Integer)
    Name = db.Column(db.String(255))
    Date = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    Salary = db.Column(db.Integer)
    Amount = db.Column(db.JSON)
    Interest = db.Column(db.JSON)
    Tenure = db.Column(db.JSON)
    Status = db.Column(db.String(255))
    Reviewer = db.Column(db.String(255))
    ReviewerID = db.Column(db.Integer)
    RejectMessage = db.Column(db.JSON)

    def __init__(self, AgentID, AgentName, CustomerID, Name, Date, Email, Address, Salary, Amount, Interest, Tenure, Status, Reviewer, ReviewerID, RejectMessage):
        self.AgentID = AgentID
        self.AgentName = AgentName
        self.CustomerID = CustomerID 
        self.Name = Name
        self.Date = Date
        self.Email = Email
        self.Address = Address
        self.Salary = Salary
        self.Amount = Amount
        self.Interest = Interest
        self.Tenure = Tenure
        self.Status = Status
        self.Reviewer = Reviewer
        self.ReviewerID = ReviewerID
        self.RejectMessage = RejectMessage
        

@login_manager.user_loader
def load_user(user_id):
    if session['Usertype'] == 'Admin':
        return Users.query.filter_by(_id=user_id).first()
    elif session['Usertype'] == 'Agent':
        return Users.query.filter_by(_id=user_id).first()
    elif session['Usertype'] == 'Customer':
        return Customers.query.filter_by(_id=user_id).first()
    return Users.query.filter_by(_id=user_id).first()

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def roles_required(*args, **kwargs):

            if current_user:

                if not current_user.Role in roles:
                    flash("You do not have permission to access this page", "warning")
                    abort(404, "You don't have permission to access this page ")
                return f(*args, **kwargs)
            else:
                flash("You do not have permission to access this page", "warning")
                abort(404)
        return roles_required
    return decorator


class Login(Form):
    Email = StringField('Email', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Password = PasswordField('Password', validators=[InputRequired(message='Required')])
    UserType = SelectField(choices=UserTypes)

class Register(Form):
    Name = StringField('Email', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Email = StringField('Email', validators=[InputRequired(message='Required'), length(min=3, max=30, message="Name should be below 30 Characters")])
    Password = PasswordField('Password', validators=[InputRequired(message='Required')])
    UserType = SelectField(choices=UserTypes)
    
@app.route("/", methods=['POST', 'GET'])
def home():
    logout_user()
    LoginForm = Login()
    if request.method == 'POST':
        Email = LoginForm.Email.data
        Password =LoginForm.Password.data
        Usertype = LoginForm.UserType.data
        if Usertype == "Admin":
            session['Usertype'] = Usertype
            user_found = Users.query.filter_by(Email=Email,Role="Admin").first()
            if user_found:
                if bcrypt.check_password_hash(user_found.Password,Password):
                    login_user(user_found)
                    return redirect(url_for("admin.AdminHome"))
                else:
                    flash("Check Password and Try Again")
            else:
                flash("Check Username and Try Again")
        elif Usertype == "Agent":
            session['Usertype'] = Usertype
            user_found = Users.query.filter_by(Email=Email,Role="Agent").first()
            if user_found:
                if bcrypt.check_password_hash(user_found.Password,Password):
                    login_user(user_found)
                    return redirect(url_for("agent.AgentHome"))
                else:
                    flash("Check Password and Try Again")
            else:
                flash("Check Username and Try Again")
                return render_template("Home.html", form=LoginForm)
        elif Usertype == "Customer":
            print(Usertype)
            session['Usertype'] = Usertype
            user_found = Customers.query.filter_by(Email=Email,Role="Customer").first()
            if user_found:
                if bcrypt.check_password_hash(user_found.Password,Password):
                    login_user(user_found)
                    return redirect("customer/{}".format(user_found._id))
                else:
                    flash("Check Password and Try Again")
            else:
                flash("Check Username and Try Again")
                return render_template("Home.html", form=LoginForm)
    return render_template("Home.html", form=LoginForm)

@app.route("/ren_Register", methods=['POST','GET'])
def ren_Register():
    if session['Admin'] == "Admin":
        LoginForm = Login()
        RegisterForm = Register()
        if request.method == 'POST':
            Name = RegisterForm.Name.data
            Email = RegisterForm.Email.data
            Password = bcrypt.generate_password_hash(RegisterForm.Password.data)
            Usertype = RegisterForm.UserType.data
            user_found = Users.query.filter_by(Email=Email,Password=Password,Role="Admin").first()
            if user_found:
                flash("User Already Exist")
                return redirect(url_for("home"))
            else:
                data = Users(Name, Email, Password, 'Admin')
                db.session.add(data)
                db.session.commit()
                flash("User Registered")
                return redirect(url_for("home"))
        return render_template("Register.html", form=LoginForm, form2 = RegisterForm)
    else:
        flash("Something went wrong!")
        return redirect(url_for("home"))

@app.route("/default_login", methods=['GET','POST'])
def default_login():
    if request.method == 'POST':
        if (request.form.get("def_id") == "Admin") & (request.form.get("def_password") == "Admin@123#"):
            session['Admin'] = "Admin"
            return redirect(url_for("ren_Register"))
        else:
            flash("Only Admin can login in that page")
            return redirect(url_for("home"))
    return render_template("DefaultLogin.html")


@app.route("/logout")
def logout():
    logout_user()
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    db.create_all()
    app.register_blueprint(admins, url_prefix="/admin")
    app.register_blueprint(agents, url_prefix="/agent")
    app.register_blueprint(customers, url_prefix="/customer")
    app.run(debug=True,port=3000)