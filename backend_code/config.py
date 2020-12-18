import os

class Config:

    #Secret Key to stop XSS and cross site forgery
    #SQLALCHEMY to define database path
    SECRET_KEY  = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    #App settings for mail service (using gmail so mail server is smtp.googlemail.com)
    MAIL_SERVER   = 'smtp.googlemail.com'
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
