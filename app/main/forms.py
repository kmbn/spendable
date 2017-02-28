import re
from flask import Markup
from flask_wtf import Form
from wtforms import StringField, SubmitField, ValidationError, DateField, \
    DecimalField, SelectField
from wtforms.validators import Required
from app.tinyutils import create_date


# Custom validators

def is_currency(form, field):
    try:
        float(field.data)
    except:
        TypeError
        raise ValidationError(Markup('Enter a valid amount like \
            <code>-5</code>, <code>-22.50</code> or <code>3.75</code>.'))


def is_date(form, field):
    if field.data != '':
        try:
            create_date(field.data)
        except:
            ValueError
            raise ValidationError(Markup('Enter a date in the format \
                <code>2017-03-28</code>.'))


class AddTransactionForm(Form):
    date = StringField('When? (default is today)', validators=[is_date])
    amount = DecimalField(Markup('How much? (expense by default; \
        start with <code>-</code> for income)'), validators=[Required()])
    description = StringField('Where or what?')
    submit = SubmitField('Add transaction')


class EditTransactionForm(Form):
    date = StringField('When?')
    amount = DecimalField('How much?', validators=[Required()])
    description = StringField('Where or what?')
    submit = SubmitField('Save edited transaction')


class CreateBudgetForm(Form):
    budget_type = SelectField('Monthly or weekly budget?', \
        choices =[('monthly', 'monthly'), ('weekly', 'weekly')])
    amount = DecimalField('How much?', validators=[Required()])
    submit = SubmitField('Create budget')


class EditBudgetForm(Form):
    budget_type = SelectField('Monthly or weekly budget?', \
        choices =[('monthly', 'monthly'), ('weekly', 'weekly')])
    amount = DecimalField('How much?', validators=[Required()])
    submit = SubmitField('Update budget')