from flask import Flask, session, redirect, url_for, render_template, flash, \
                  Blueprint
import ujson
from app.db import *
from . import admin
from app.decorators import login_required


@admin.route('/')
@login_required
def view_admin():


    return render_template('admin.html')


@admin.route('/restart')
@login_required
def restart():
    """
    Delete all transactions and start fresh.
    Budget and other settings remain as before.

    """

    get_table('transactions').purge()

    flash('Transactions deleted. Enjoy your fresh start!')

    return redirect(url_for('main.home'))
