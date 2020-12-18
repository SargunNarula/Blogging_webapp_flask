from flask import Blueprint
from flask import render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error_templates/404_html_code.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error_templates/403_html_code.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error_templates/500_html_code.html'), 500



