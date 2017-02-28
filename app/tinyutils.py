from datetime import datetime


"""
TinyDB can't handle datetime objects, so we need to convert back and forth
between datetime objects and strings.
"""


def create_timestamp(current_time):
    """Convert datetime date to string."""
    timestamp = datetime.strftime(current_time, '%Y-%m-%d')
    return timestamp


def create_date(string):
    """Convert string to datetime date."""
    date = datetime.strptime(string, '%Y-%m-%d').date()
    return date