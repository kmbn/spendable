from app.db import *


def update_by_eid(table, key, new_data, current_user):
    eid = get_table(table).update({key: new_data}, \
        eids=[current_user]) # use session.get('user_id') for multi-user app
    updated_element = get_table(table).get(eid=eid[0])
    updated_data = updated_element[key]
    return updated_data


def get_user_id(email):
    user_id = get_element_id('auth', Query().email == email)
    return user_id


def create_user(email, password_hash):
    """ Insert a new user and get the element id of the new record. """
    eid = insert_record('auth', {'email': email, \
        'password_hash': password_hash})
    return eid


def user_is_registered():
    """ Returns True if a user is registered, False if not. """
    if get_table('auth').search(Query().email.exists()):
        return True
    else:
        return False