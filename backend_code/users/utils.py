import secrets
import os

from PIL import Image

from flask import url_for
from flask import current_app

from flask_mail import Message

#from backend_code import app
from backend_code import mail 






#To save new picture as profilepic
def save_picture(new_picture):
    random_hex = secrets.token_hex(8)
    # _ --> file_name
    
    _ , f_ext = os.path.splitext(new_picture.filename) 
    picture_fullname = random_hex + f_ext
    picture_path     = os.path.join(current_app.root_path, 'static/pics/', picture_fullname) 

    #Resizing the picture using pillow
    output_size = (125,125)
    i = Image.open(new_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fullname


def send_email(user):
    token = user.get_token()
    msg = Message('Password Reset Request', sender="noreply@demo.com", recipients=[user.email])
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)