import datetime
import random
import string

import sqlalchemy
from sqlalchemy import orm
from passlib.hash import bcrypt

import models
import db


"""
fixtures.py
This is a module for populating testing data into the db.  It's used in two places:
1 - the test suite
2 - as a standalone, whenever the dev version of the site is being data wacky or you want to add new testing data.

"""

def lorem(n):
    return " ".join("""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?""".split(
        " ")[0:n])

engine = None
session = None

def init():
    global engine
    global session
    engine = sqlalchemy.create_engine(db.db_conn_string)
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)
    sessionmaker = orm.sessionmaker(bind=engine)
    session = sessionmaker()


def pick_member():
    members = session.query(models.Member).all()
    return random.choice(members)

vowels = ['a', 'e', 'i', 'o', 'u']
consonants = [i for i in string.ascii_lowercase if i not in vowels]

def makeaname(length):
    name = []
    name.append(random.choice(string.ascii_uppercase))
    for i in range(length):
        if name[-1].lower() == 'q':
            name.append('u')
        elif name[-1].lower() in vowels:
            name.append(random.choice(consonants))
        else:
            name.append(random.choice(vowels))
    return ''.join(name)

def makeanemail(name):
    return str(name + "@gmail.com")

def garble(length):
    return "".join(random.choice(string.ascii_uppercase)
                   for i in range(length))


def generate_person():
    person = models.Member(
        name=makeaname(8),
        email=makeanemail(makeaname(8)),
        created=datetime.datetime.now(),
        passhash = bcrypt.hash("pass"),
        admin=False
    ) 
    session.add(person)
    session.commit()

def crowd(numpeople):
    for i in range(numpeople):
        generate_person()

def people():
    tom = models.Member(
        created=datetime.datetime.now(),
        passhash=bcrypt.hash("pass"),
        email="tom@gmail.com",
        admin=False
    )
    session.add(tom)
    session.commit()

def gogogadget():
    init()
    people()
    crowd(50)

if __name__ == "__main__":
    gogogadget()
