
#Importing render_template from flask module to connect html files with backend

from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import request
from flask import abort

from flask_login import login_user
from flask_login import current_user 
from flask_login import logout_user
from flask_login import login_required

from flask_mail import Message

from backend_code import app
from backend_code import db
from backend_code import bcrypt
from backend_code import mail 

from backend_code.forms import RegistrationForm
from backend_code.forms import LoginForm
from backend_code.forms import UpdateForm
from backend_code.forms import CreatePost
from backend_code.forms import RequestResetForm
from backend_code.forms import ResetPasswordForm

from backend_code.models import User
from backend_code.models import Post

from PIL import Image

import secrets
import os


db.create_all()


#Static Info
blogs_info = [
    {
        "name": "Sargun",
        "title": "Blog Post 1",
        "content": "it is working",
        "date": "15th sep 2020"
    }
    ,
    {
        "name": "Narula",
        "title": "Post 2",
        "content": "it is working again",
        "date": "15th sep 2020"
    }
]



#app.route are decorators in flask which hold functions to run when that webpage is opened
#We can use multiple decorators to set different routes to one page only ( "/"  and home both show same page)










   

            




