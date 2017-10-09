import re

def provjeraUsername(username) :
    if re.match("^[a-zA-Z0-9_.-]{3,15}$", username):
        return True
    return False

def provjeraPasswordJednakost(pass1,pass2) :
    if pass1==pass2 :
        return True
    return False


def provjeraPassword(password) :
    if re.match("^.*(?=.{4,10})(?=.*\d)(?=.*[a-zA-Z]).*$",password):
        return True
    return False

def provjeraIme(ime) :
    print(ime)
    if re.match("^[a-zA-Z]+$",ime):
        return True
    return False

def provjeraEmail(email):
    if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email):
        return True
    return False
