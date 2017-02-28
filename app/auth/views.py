# -*- coding: utf-8 -*-
from flask import Flask, session, redirect, url_for, render_template, flash, \
                  Blueprint, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import ujson
from datetime import datetime
from app.db import *
from . import auth, pwd_context
from .forms import ChangeEmailForm, ChangePasswordForm, \
                       RegistrationForm, LoginForm, ResetPasswordForm, \
                       SetNewPasswordForm
from app.mail import send_email
from app.decorators import login_required
from .models import user_is_registered, get_user_id, update_by_eid, \
    create_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('main.home'))
    if not user_is_registered():
        flash('You need to register first.')
        return redirect(url_for('auth.register'))

    form = LoginForm()

    if form.validate_on_submit():
        session['logged_in'] = True
        session['user_id'] = get_user_id(form.email.data)
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        else:
            return redirect(url_for('main.home'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():

    session['logged_in'] = None
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    ''' Register user and create pagination table with one page
    and no entries.'''
    if user_is_registered():
        flash('A user is already registered. Log in.')
        return redirect(url_for('auth.login'))

    form = RegistrationForm()

    if form.validate_on_submit():
        password_hash = pwd_context.hash(form.password.data)
        # Create account and get creator id
        creator_id = create_user(form.email.data, password_hash)
        # Create site details
        # Create empty pagination table
        insert_record('pagination', {'page': 1, 'transactions': None})
        flash('Registration successful. You can login now.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_id = get_user_id(form.email.data)
        token = generate_confirmation_token(user_id)
        send_email(email, 'Link to reset your password',
                   'email/reset_password', token=token)
        flash('Your password reset token has been sent.')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def confirm_password_reset(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('auth.request_reset'))
    if not data.get('confirm'):
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('auth.request_reset'))
    user_id = data.get('confirm')
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        new_password_hash = pwd_context.hash(form.new_password.data)
        update_by_eid('auth', 'password_hash', new_password_hash, user_id)
        flash('Password updated—you can now log in.')
        return redirect(url_for('auth.login'))

    return render_template('set_new_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        new_email = form.new_email.data
        user_id = 1 # use session.get('user_id') for multi-user
        update_by_eid('auth', 'email', new_email, user_id)
        flash('Your email address has been updated.')
        return redirect(url_for('admin.view_admin'))

    return render_template('change_email.html', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_password_hash = pwd_context.hash(form.new_password.data)
        user_id = 1 # use session.get('user_id') for multi-user
        update_by_eid('auth', 'password_hash', new_password_hash, user_id)
        flash('Your password has been updated.')
        return redirect(url_for('admin.view_admin'))

    return render_template('change_password.html', form=form)


def generate_confirmation_token(user_id, expiration=3600):
    serial = Serializer(current_app.config['SECRET_KEY'], expiration)
    return serial.dumps({'confirm': user_id})