
from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request

from flask_login import login_user
from flask_login import current_user 
from flask_login import logout_user
from flask_login import login_required

from backend_code import db
from backend_code import bcrypt

from backend_code.models import User
from backend_code.models import Post

from backend_code.users.forms import RegistrationForm
from backend_code.users.forms import LoginForm
from backend_code.users.forms import UpdateForm
from backend_code.users.forms import RequestResetForm
from backend_code.users.forms import ResetPasswordForm


from backend_code.users.utils import save_picture 
from backend_code.users.utils import send_email

users = Blueprint('users',__name__)

#

                                            # Routes

                                        # 1. register
                                        # 2. login
                                        # 3. logout
                                        # 4. account 
                                        # 5. user_posts


@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_text'))
    else:
        form_instance = RegistrationForm()
        if form_instance.validate_on_submit():

            #hash the password and save it to database
            hashed_pw = bcrypt.generate_password_hash(form_instance.password.data).decode('utf-8')
            user = User(username=form_instance.username.data, email=form_instance.email.data, password=hashed_pw)
            db.session.add(user)
            db.session.commit()

            #flash a message and redirect to login page
            flash("Account Created Successfully", 'success')
            return redirect(url_for('users.login'))
        return render_template('register_html_code.html', title="Register", form=form_instance)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_text'))
    else:
        login_instance = LoginForm()
        if login_instance.validate_on_submit():

            user = User.query.filter_by(email=login_instance.email.data).first()
            if user and bcrypt.check_password_hash(user.password, login_instance.password.data):
                login_user(user, remember=login_instance.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home_text'))
            else:
                flash("Login Incorrect", 'danger') 
        return render_template('login_html_code.html', title="Login", form=login_instance)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home_text'))


@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    account_instance = UpdateForm()
    if account_instance.validate_on_submit():
        if account_instance.picture.data:
            picture_file = save_picture(account_instance.picture.data)
            current_user.image_file = picture_file

        current_user.username = account_instance.username.data
        current_user.email = account_instance.email.data
        db.session.commit()
        flash('Your Account has been upadted','success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        account_instance.username.data = current_user.username
        account_instance.email.data = current_user.email

    image_file = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account_html_code.html', title="Account", form=account_instance, image_file=image_file)

@users.route("/user/<string:username>")
def user_posts(username):

    page = request.args.get('page', 1, type=int)
    user_instance = User.query.filter_by(username=username).first_or_404()

    blogs = Post.query\
        .filter_by(author=user_instance)\
        .order_by(Post.date.desc())\
        .paginate(per_page=5, page=page)
    

    return render_template("user_posts_html_code.html",posts=blogs, title="User Posts", user=user_instance) 



# 
                                            # Password Routes
                                        
                                        # 6. reset request
                                        # 7. reset password
        # <!-------------------------------------------------------------------------------------------------->



@users.route("/reset_password", methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_text'))
    request_instance = RequestResetForm()
    if request_instance.validate_on_submit():
        user = User.query.filter_by(email=request_instance.email.data).first()
        
        #Now we will send user the email
        send_email(user)
        flash('A mail has been sent to your Email Account', 'info')
        return redirect(url_for('users.login'))


    return render_template('reset_request_html_code.html', title="Reset Password", form=request_instance)

@users.route("/reset_password/<token>", methods=["GET","POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home_text'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    
    password_instance = ResetPasswordForm()
    if password_instance.validate_on_submit():

        #hash the password and save it to database
        hashed_pw = bcrypt.generate_password_hash(password_instance.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()

        #flash a message and redirect to login page
        flash("Reset Password Successfully", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password_html_code.html', title="Reset Password", form=password_instance)