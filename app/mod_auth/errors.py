from flask import render_template
from . import auth


@auth.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@auth.errorhandler(500)
def internal_error(error):
    return render_template('500.html')