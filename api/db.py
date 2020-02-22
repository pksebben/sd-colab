

import plugin
import models

# DB
db_conn_string = "sqlite:///foo.db"
db = None

def init(app):
    # this creates what would otherwise be db.web
    global db
    db = plugin.SQLAlchemy(app, db_conn_string)
    models.Base.metadata.create_all(db.engine)
