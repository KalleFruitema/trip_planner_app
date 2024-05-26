from uuid import uuid4
from forms import LoginForm, RegistrationForm, JoinPlanForm, CreatePlanForm
from models import User, Plan
from database import db

from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = b'\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session["logged_in"] = True
            session["username"] = user.username
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            form.password.data = ''
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            user = User(username=form.username.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'danger')
            form.username.data = ''
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route("/create_plan", methods=['GET', 'POST'])
def create_plan():
    form = CreatePlanForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        if date.strftime(start_date, format='%Y-%m-%d') > date.strftime(end_date, format='%Y-%m-%d'):
            flash('Start date is before end date.', 'danger')
        else:
            plan_code = str(uuid4())
            user = User.query.filter_by(username=session['username']).first()
            plan = Plan(name=name, description=description, plan_code=plan_code, start_date=start_date, end_date=end_date, owner_id=user.id)
            if user:
                plan.users.append(user)
                db.session.add(plan)
                db.session.commit()
                flash('Plan created successfully!', 'success')
                return redirect(url_for('view_plan', plan_code=plan.plan_code))
            else:
                flash('You need to be logged in to create a plan.', 'danger')
                return redirect(url_for("home"))
        
    return render_template("create_plan.html",
                           form=form)
    
    
@app.route('/plan/<plan_code>', methods=['GET', 'POST'])
def view_plan(plan_code):
    plan = Plan.query.filter_by(plan_code=plan_code).first_or_404()
    user = User.query.filter_by(username=session['username']).first()
    if request.method == "POST":
        to_kick_id = request.form.get("to_kick_id")
        print(to_kick_id)
        user_to_kick = User.query.get(to_kick_id)
        print(user_to_kick.username)
        plan.users.remove(user_to_kick)
        db.session.commit()
        flash(f"User \"{user_to_kick.username}\" kicked succesfully!", "succes")
    return render_template('view_plan.html', plan=plan, viewer=user)


@app.route('/plan/<plan_code>/leave', methods=['GET', 'POST'])
def leave_plan(plan_code):
    plan = Plan.query.filter_by(plan_code=plan_code).first_or_404()
    user = User.query.filter_by(username=session['username']).first()
    if user:
        if plan and user in plan.users:
            plan.users.remove(user)
            db.session.commit()
            flash('You have left the plan.', 'success')
            return redirect(url_for("home"))
        else:
            flash('You are not a member of this plan.', 'danger')
    else:
        flash('You need to be logged in to leave a plan.', 'danger')
    return redirect(url_for("view_plan"))


@app.route('/plan/<plan_code>/disband', methods=['GET', 'POST'])
def disband_plan(plan_code):
    plan = Plan.query.filter_by(plan_code=plan_code).first_or_404()
    user = User.query.filter_by(username=session['username']).first()
    if user:
        if plan and user in plan.users:
            db.session.delete(plan)
            db.session.commit()
            flash('You have disbanded the plan.', 'success')
            return redirect(url_for("home"))
        else:
            flash('You are not a member of this plan.', 'danger')
    else:
        flash('You need to be logged in as the owner to disband a plan.', 'danger')
    return redirect(url_for("view_plan"))


@app.route("/", methods=['GET', 'POST'])
def home():
    form = JoinPlanForm()
    plans = []
    if "logged_in" in session and session["logged_in"]:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            plans = user.plans.all()
    if form.validate_on_submit():
        existing_plan = Plan.query.filter_by(plan_code=form.plan_code.data).first()
        if existing_plan is None:
            flash('Plan with this code doesnt exist. Perhaps you made a typo?', 'danger')
        else:
            user = User.query.filter_by(username=session['username']).first()
            if user:
                existing_plan.users.append(user)
                db.session.add(existing_plan)
                db.session.commit()
                return redirect(url_for('view_plan', plan_code=existing_plan.plan_code))
                
            
    return render_template("home.html",
                           username="Kalle",
                           form=form,
                           plans=plans)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
