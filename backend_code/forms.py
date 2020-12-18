from flask_wtf import FlaskForm

from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed

from wtforms import StringField 
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import TextAreaField

from wtforms.validators import DataRequired 
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

from backend_code.models import User, Post

from flask_login         import current_user



