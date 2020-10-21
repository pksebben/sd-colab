from __future__ import print_function
import logging
import sys

import structlog
from structlog import twisted
from structlog.twisted import LoggerFactory
from flask import Flask
from twisted.internet import reactor, endpoints
from twisted.python import log
from twisted.web import server, wsgi

import db
import container
import api
"""
TODO:
refactor these:

"""
logger = structlog.get_logger()

app = Flask(__name__)

@app.route('/')
def helloworld():
    return """<h1>Sup, dawg.</h1>"""

# from app.py pyg
def init():
    app.register_blueprint(api.api)
    # register all routes
    # maybe nothing else.
    return app


# from run.py pyg
def main():
    log.msg("RUN main")
    # initialize app
    init()                      
    # initialize db
    log.msg("RUN db.init(app)")
    db.init(app)
    # this is probably pointless until there's a GUI of sorts
    app.jinja_env.auto_reload = True
    log.msg("RUN container.run")
    container.run(app=app, address="tcp:8080", debug=True)

# from run.py
if __name__ == "__main__": 
    log.msg("RUN __main__")
    structlog.configure(
        processors=[twisted.EventAdapter()],
        logger_factory=twisted.LoggerFactory(),
        wrapper_class=twisted.BoundLogger,
        cache_logger_on_first_use=True
    )
    log.startLogging(sys.stderr)
    log.msg("LOG STARTED")
    main()
