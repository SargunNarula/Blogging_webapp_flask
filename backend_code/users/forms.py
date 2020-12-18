from flask_wtf import FlaskForm

from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed

from wtforms import StringField 
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField

from wtforms.validators import DataRequired 
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

from flask_login import current_user 

from backend_code.models import User

class RegistrationForm(FlaskForm):
    username = StringField  ('Username'  , validators=[DataRequired(),Length(min=2,max=20) ])
    email    = StringField  ('Email'     , validators=[DataRequired(), Email() ])
    password = PasswordField('Password'  , validators=[DataRequired()])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password') ])
    submit   = SubmitField('Sign Up')

        #             CUSTOM VALIDATION CHECKS
        # !---------------------------------------------- 
        # We could have made check in routes.py
        # but this method is much more efficient
        # here FlaskForm class (from which this class has inherited)
        # itself calls all the custom validation functions defined
        # just the name syntax should be --->>> validate_something()

    
    
    # 1.) To check if username already exists
    def validate_username(self, username):
        present = User.query.filter_by(username=username.data).first()
        if present:
            raise ValidationError('Username Already Exists')

    # 2.) To check if email  already exists
    def validate_email(self, email):
        present = User.query.filter_by(email=email.data).first()
        if present:
            raise ValidationError('Email Already Exists')
        
class LoginForm(FlaskForm):
    #username = StringField  ('Username'  , validators=[DataRequired(),Length(min=2,max=20) ])
    email     = StringField  ('Email'     , validators=[DataRequired(), Email() ])
    password  = PasswordField('Password'  , validators=[DataRequired()])
    #confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password') ])
    remember  = BooleanField('       RememberMe')
    submit    = SubmitField('Login')
    
#To update Account Info
class UpdateForm(FlaskForm):

    username = StringField  ('Username'        , validators=[DataRequired(),Length(min=2,max=20) ])
    email    = StringField  ('Email'           , validators=[DataRequired(), Email() ])
    picture  = FileField    ('Profile Picture' , validators=[FileAllowed(['jpg','png','jpeg'])])
    submit   = SubmitField('Submit changes')
 
        
        #             CUSTOM VALIDATION CHECKS
        # !---------------------------------------------- 
        # We could have made check in routes.py
        # but this method is much more efficient
        # here FlaskForm class (from which this class has inherited)
        # itself calls all the custom validation functions defined
        # just the name syntax should be --->>> validate_something()

    
    
    # 1.) To check if username already exists
    def validate_username(self, username):
        if username != current_user.username:
            present = User.query.filter_by(username=username.data).first()
            if present:
                raise ValidationError('Username Already Exists')

    # 2.) To check if email  already exists
    def validate_email(self, email):
        # To check to database only when updated info is new otherwise skip
        if email != current_user.email:
            present = User.query.filter_by(email=email.data).first()
            if present:
                raise ValidationError('Email Already Exists')

class RequestResetForm(FlaskForm):
    email    = StringField  ('Email'     , validators=[DataRequired(), Email() ])
    submit   = SubmitField('Password Reset')

    def validate_email(self, email):
        present = User.query.filter_by(email=email.data).first()
        if present is None:
            raise ValidationError('No email like this')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password'  , validators=[DataRequired()])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password') ])    
    submit   = SubmitField('Reset Password')