from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file, Response, make_response
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import secrets

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = False
app.secret_key = 'task'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'payey11431@egela.com'
app.config['MAIL_PASSWORD'] = '123456'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    uploaded_by = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    
db.init_app(app)

with app.app_context():
    db.create_all()
    
# hashed_password = generate_password_hash('tushank123')
# operational_user = User(username='Tushank', password_hash=hashed_password, email='tushank121@gmail.com', verified=True)

# with app.app_context():
#     db.session.add(operational_user)
#     db.session.commit()

# print("Operational user added.")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        session["username"] = username
        
        if user.username == "Tushank":
            return redirect(url_for("file"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/file")
def file():
    if "username" not in session or session["username"] != "Tushank":
        flash("Access Denied")
        return redirect(url_for("login"))
    return render_template("file.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No elected file")
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_data = file.read()  # Stream file content directly into variable
        db.session.add(File(filename=filename, file_data=file_data, uploaded_by=session["username"], uploaded_at=datetime.datetime.now()))
        db.session.commit()
        flash("File uploaded successfully")
        return redirect(url_for("file"))
    
@app.route("/sign", methods=["GET", "POST"])
def signUp():
    if request.method == "POST":
        existing_user = User.query.filter_by(username=request.form["username"]).first()
        if existing_user:
            flash("Username already taken.")
            return redirect(url_for("signUp"))  # Redirect back to the sign-up page
        
        token = secrets.token_hex(16)
        user = User(username=request.form["username"], password_hash=generate_password_hash(request.form["password"]), email=request.form["email"])
        db.session.add(user)
        db.session.commit()
        
        msg = Message("Verify your Email", recipients=[user.email])
        msg.body = f"Please click this link to verify your email: http://localhost:5000/verify/{token}"
        mail.send(msg)
        return redirect(url_for("login"))  # Redirect to the login page after successful signup
    else:
        return render_template("signUp.html")

@app.route("/verify/<token>")
def verify_email(token):
    user = User.query.filter_by(email=token).first()
    if user:
        user.verified = True
        db.session.commit()
        return "Your email has been verified"
    else:
        return "Verification failed", 400

@app.route("/clientLogin", methods=["GET","POST"])
def clientLogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password")
            return render_template("clientLogin.html")
        else:
            session["username"] = username
            session["password"] = password
            return redirect(url_for("innerHomePage"))
    return render_template("clientLogin.html")

@app.route("/innerHomePage")
def innerHomePage():
    uploaded_name = "Tushank"
    user_files = File.query.filter_by(uploaded_by=uploaded_name).all()
    print([f.filename for f in user_files])  # Debugging line to print filenames
    return render_template("innerHomePage.html", files=user_files)

@app.route("/download_file/<filename>")
def download_file(filename):
    file_record = File.query.filter_by(filename=filename).first()
    if file_record:
        file_data = file_record.file_data
        response = make_response(send_file(BytesIO(file_data), mimetype='application/octet-stream'))
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    else:
        pass
        
if __name__ == "__main__":
    app.run(debug=True)