import ujson
from datetime import datetime, timedelta
from tinydb import TinyDB
from db import *
from tinyutils import *


class Transaction(object):

    def __init__(self, date, amount, description, eid=None):
        self.date = date
        self.amount = amount
        self.description = description
        self.id = eid


    def add(self):
        eid = insert_record('transactions', {'date': self.date, \
            'amount': self.amount, \
            'description': self.description})
        new_id = get_table('transactions').update({'id': eid}, \
            eids=[eid])
        self.id = new_id[0]
        return self.id


    def view(eid):
        result = get_table('transactions').get(eid=eid)
        print(result)
        transaction = Transaction(result['date'], result['amount'], \
            result['description'], result['id'])
        return transaction


    def update(self):
        eid = get_table('transactions').update({'date': self.date, \
            'amount': self.amount, \
            'description': self.description}, eids=[self.id])
        return eid[0]


    def delete(self):
        eid = get_table('transactions').remove(eids=[self.id])
        return eid[0]


class Budget(object):

    def __init__(self, budget_type, amount):
        self.type = budget_type
        self.amount = amount


    def add(self):
        eid = insert_record('budget', {'type': self.type, \
            'amount': self.amount})
        return eid


    def view():
        result = get_table('budget').get(eid=1)
        budget = Budget(result['type'], result['amount'])
        return budget


    def update(self):
        eid = get_table('budget').update({'type': self.type, \
            'amount': self.amount}, eids=[1])
        return eid[0]


    def delete(self):
        eid = get_table('budget').remove(eids=[1])
        return eid[0]


class Report(object):

    def __init__(self, date):
        self.date = date


    def sum_up(transactions):
        amounts = [x['amount'] for x in transactions]
        total = sum(amounts)
        return total


    def inflow(transactions):
        amounts = [x['amount'] for x in transactions if x['amount'] > 0]
        total = sum(amounts)
        return total


    def outflow(transactions):
        amounts = [x['amount'] for x in transactions if x['amount'] < 0]
        total = sum(amounts)
        return total


    def transactions():
        transactions = get_table('transactions').all()
        transactions = transactions[::-1]
        return transactions


    def balance(self):
        transactions = get_table('transactions').all()
        self.balance = Report.sum_up(transactions)
        return self.balance


    def remaining(self):

        budget = Budget.view()
        today = create_timestamp(datetime.utcnow().date())

        if budget.type == 'monthly':
            transactions = get_table('transactions').\
            search((Query().date.all([today[:7]])))
            self.remaining = budget.amount + Report.outflow(transactions)

        if budget.type == 'weekly':
            end = today
            end_date = create_date(end)
            date_index = datetime.weekday(end_date)
            day_range = 0 - date_index # 0 if monday, -6 if sunday
            start_date = end_date + timedelta(days=day_range)
            start = create_timestamp(start_date)
            transactions = get_table('transactions').\
                search((Query().date >= start) & (Query().date <= end))
            self.remaining = budget.amount + Report.outflow(transactions)

        return self.remaining


    def overview(self):
        Report.day(self)
        Report.week(self)
        Report.month(self)
        Report.balance(self)
        Report.remaining(self)
        return self


    def day(self):
        self.transactions = get_table('transactions').\
            search(Query().date == self.date)
        self.daily_outflow = Report.outflow(self.transactions)
        self.daily_inflow = Report.inflow(self.transactions)
        Report.balance(self)
        Report.remaining(self)
        return self


    def week(self):
        end = self.date
        end_date = create_date(end)
        date_index = datetime.weekday(end_date)
        day_range = 0 - date_index # 0 if monday, -6 if sunday
        start_date = end_date + timedelta(days=day_range)
        start = create_timestamp(start_date)
        self.transactions = get_table('transactions').\
            search((Query().date >= start) & (Query().date <= end))
        self.weekly_outflow = Report.outflow(self.transactions)
        self.weekly_inflow = Report.inflow(self.transactions)
        Report.balance(self)
        Report.remaining(self)
        return self


    def month(self):
        self.transactions = get_table('transactions').\
            search((Query().date.all([self.date[:7]])))
        self.monthly_outflow = Report.outflow(self.transactions)
        self.monthly_inflow = Report.inflow(self.transactions)
        Report.balance(self)
        Report.remaining(self)
        return self


class User(object):

    def __init__(self, email, password_hash, currency_pref='euro'):
        self.email = email
        self.password_hash = password_hash
        self.currency_pref = currency_pref


    def add(self):
        eid = insert_record('users', {'email': self.email, \
            'password_hash': self.password_hash, \
            'currency_pref': self.currency_pref})
        new_id = get_table('users').update({'id': eid}, \
            eids=[eid])
        self.id = new_id[0]
        return self.id


    def view(eid):
        result = get_table('users').get(eid=eid)
        user = User(result['email'], result['password_hash'], \
            result['currency_pref'], result['id'])
        return user


    def update(self):
        eid = get_table('users').update({'email': self.email, \
            'password_hash': self.password_hash, \
            'currency_pref': self.currency_pref}, eids=[self.id])
        return eid[0]


    def delete(self):
        eid = get_table('users').remove(eids=[self.id])
        return eid[0]