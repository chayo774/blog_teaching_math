from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, login_required, logout_user
from .webforms import UserForm, LoginForm
from ..models import Users
from ..extensions import db, bcrypt
from . import auth_bp


@auth_bp.route("/sign", methods=['GET','POST'])
def sign():
    formulario= UserForm()
    if formulario.validate_on_submit():
        user=Users.query.filter_by(email=formulario.email.data).first()
        if user is None:
            hashed_pw=bcrypt.generate_password_hash(formulario.password_hash.data).decode('utf-8')
            user=Users(username=formulario.username.data,name=formulario.name.data, email=formulario.email.data, about_me=formulario.aboutme.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        formulario.name.data=''    
        formulario.username.data=''    
        formulario.email.data='' 
        formulario.password_hash.data='' 
        flash("Usuario ha sido creado")
        return redirect(url_for('auth.login'))
    return render_template("auth/sign.html", form=formulario)

@auth_bp.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull!!")
                return redirect(url_for('public.index'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")        
    our_users = Users.query.order_by(Users.date_added)
    return render_template("auth/login.html",form =form, usuarios=our_users) 
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    # login_successful = session.pop('login_successful', False)
    login_successful = session.pop('login_successful', True)
    return render_template("auth/dashboard.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Closed Session...!")
    return redirect(url_for('auth.login'))
