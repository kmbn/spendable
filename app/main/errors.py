from flask import render_template
from tinydb import Query
from app.db import get_record
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    details = get_details()
    content = {'details': details, 'error': e}
    return render_template('404.html', content=content), 404


@main.app_errorhandler(405)
def page_not_found(e):
    details = get_details()
    content = {'details': details, 'error': e}
    return render_template('405.html', content=content), 405


@main.app_errorhandler(500)
def internal_server_error(e):
    details = get_details()
    content = {'details': details, 'error': e}
    return render_template('500.html', content=content), 500