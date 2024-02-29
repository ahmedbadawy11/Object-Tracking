from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from .models import user
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        
        email=request.form.get("username")
        password=request.form.get("password")

        user_search=user.query.filter_by(email=email).first()
        if user_search:
            if check_password_hash(user_search.password,password):
                if request.headers.get('User-Agent') == 'Postman' or 'Mozilla' not in request.headers.get('User-Agent'):
                    return jsonify({'message': 'Logged in successfully'})
                else:
                    flash("Logged in successfully",category="success")
                    login_user(user_search,remember=True)
                    return redirect(url_for("views.upload"))

            else :
                 # Return a JSON response for Postman or non-browser clients
                if request.headers.get('User-Agent') == 'Postman' or 'Mozilla' not in request.headers.get('User-Agent'):
                    return jsonify({'message': 'Incorrect Password, try again'})
                else:
                    flash("Incorrect Password, try again.", category="Error")
        else :
             # Return a JSON response for Postman or non-browser clients
            if request.headers.get('User-Agent') == 'Postman' or 'Mozilla' not in request.headers.get('User-Agent'):
                return jsonify({'message': 'Email does not exist'})
            else:
                flash("Email does not exist.", category="Error")

    return render_template("login.html")


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    
    if request.method=='POST':
        name=request.form.get("name")
        email=request.form.get("email")
        password1=request.form.get("password")
        password2=request.form.get("password2")
        
        user_check=user.query.filter_by(email=email).first()
        if user_check:
            flash('Email already exists.',category='Error')

        elif len(name)<2:
            flash('Your Name must be greater than 2 char.',category='Error')
        elif len(email)<4:
            flash('Your email must be greater than 4 char. ',category='Error')

        elif len(password1)<7:
            flash('Your password must be greater than 7 char. ',category='Error')
        elif password1!=password2:
            flash('passwords don\'t match. ',category='Error')
        else:
            New_user=user(email=email,name=name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(New_user)
            db.session.commit()
            login_user(user_check,remember=True)
            flash('account  Created. ',category='success')
            return redirect(url_for("views.home"))

    # return "<p>sign-up</p>"
    return render_template("sign-up.html")



@auth.route('/logout')
@login_required #this mean that the user should login before logout
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for("auth.login"))