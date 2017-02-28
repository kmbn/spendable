import os
from flask import Flask, session, g, redirect, url_for, request, \
                  render_template, flash, Blueprint, current_app, abort
from flask_bootstrap import Bootstrap
from datetime import datetime
import ujson
from app.db import *
from . import main
from .forms import AddTransactionForm, EditTransactionForm, \
    CreateBudgetForm, EditBudgetForm
from app.decorators import login_required
from .models import *
from app.tinyutils import *
from app.filters import decimate


@main.route('/', methods=['GET', 'POST'])
def home():
    """
    Homepage; displays current balance and form for adding new transactions.
    """

    if not session.get('logged_in'):
        return render_template('welcome.html')

    form = AddTransactionForm()

    if form.validate_on_submit():
        if form.date.data == '':
            date = datetime.strftime(datetime.utcnow().date(), '%Y-%m-%d')
        else:
            date = form.date.data

        # Hack to make entering expenses faster
        amount = -1 * float(form.amount.data)

        transaction = Transaction(date, amount, \
            form.description.data)
        transaction.add()
        return redirect(url_for('main.home'))

    report = Report(create_timestamp(datetime.utcnow().date())).overview()
    budget = Budget.view()
    return render_template('home.html', report=report, form=form, \
        budget=budget)


@main.route('transactions')
@login_required
def view_transactions():

    transactions = Report.transactions()

    return render_template('transactions.html', transactions=transactions)


@main.route('transaction/<sid>', methods=['GET', 'POST'])
@login_required
def transaction(sid):
    """
    Displays and processes form form for editing a single transaction.
    """

    try:
        int(sid)
    except:
        TypeError
        print('type')
        return abort(404)

    eid = int(sid)

    if not Transaction.view(eid):
        print('none')
        return abort(404)

    transaction = Transaction.view(eid)

    form = EditTransactionForm()

    if form.validate_on_submit():
        transaction.date = form.date.data
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.update()
        return redirect(url_for('main.home'))

    # Add default text to form
    form.date.default = transaction.date
    form.amount.default = transaction.amount
    form.description.default = transaction.description
    form.process()

    return render_template('edit_transaction.html', transaction=transaction, form=form)


@main.route('budget')
@login_required
def view_budget():
    """
    View budget with link to edit.
    """

    budget = Budget.view()

    return render_template('budget.html', budget=budget)


@main.route('budget/edit', methods=['GET', 'POST'])
@login_required
def edit_budget():
    """
    Display and process form for editing budget.
    """

    budget = Budget.view()

    form = EditBudgetForm()

    if form.validate_on_submit():
        budget.type = form.budget_type.data
        budget.amount = form.amount.data
        budget.update()
        flash('Budget updated.')
        return redirect(url_for('main.home'))

    # Add default text to form
    form.budget_type.default = budget.type
    form.amount.default = budget.amount
    form.process()

    return render_template('edit_budget.html', budget=budget, form=form)


@main.route('budget/create', methods=['GET', 'POST'])
@login_required
def create_budget():
    """
    Display and process form for creating budget.
    """

    form = CreateBudgetForm()

    if form.validate_on_submit():
        amount = float(form.amount.data)
        budget = Budget(form.budget_type.data, amount)
        budget.add()
        flash('Budget created.')
        return redirect(url_for('main.home'))

    return render_template('edit_budget.html', form=form)


@main.route('report/<date>')
@login_required
def view_day(date):
    """
    Returns a report for a given date.
    """

    try:
        create_date(date)
    except:
        TypeError
        return abort(404)

    if create_date(date) > datetime.utcnow().date():
        return abort(404)

    report = Report(date).day()

    return render_template('page.html', report=report)


@main.route('report/week/<date>')
@login_required
def view_week(date):
    """
    Returns a report for a given week based on the last day in the week.
    """

    try:
        create_date(date)
    except:
        TypeError
        return abort(404)

    if create_date(date) > datetime.utcnow().date():
        return abort(404)

    report = Report(date).week()

    return render_template('week.html', report=report)


@main.route('report/month/<date>')
@login_required
def view_month(date):
    """
    Returns a report for a given month.
    """

    try:
        create_date(date)
    except:
        TypeError
        return abort(404)

    if create_date(date) > datetime.utcnow().date():
        return abort(404)

    report = Report(date).week()

    return render_template('week.html', report=report)