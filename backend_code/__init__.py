#Importing Flask class from flask module

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt     import Bcrypt
from flask_login      import LoginManager
from flask_mail       import Mail

from backend_code.config import Config

import re



#Creating an instance of flask class also if this file is run directly then __name__ = __main__
#Config is a class for Configuration
  
        #app = Flask(__name__)
        #app.config.from_object(Config)


#Creating a Database Instance
db = SQLAlchemy()

#Creating a Hash Instance
bcrypt = Bcrypt()

#Creating a login Instance
login_manager = LoginManager()

#To set the route of login_required decorator
login_manager.login_view = 'users.login'

#If user is not logged in and so a message is displayed everytime @login_Required is encountered
#so to customize the message we set its category
login_manager.login_message_category = 'info'

#App settings for mail service (using gmail so mail server is smtp.googlemail.com)
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    #Calling and Registering Blueprints
    from backend_code.users.routes import users
    from backend_code.posts.routes import posts
    from backend_code.main.routes  import main
    from backend_code.errors.handlers import errors 

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
