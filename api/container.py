import logging
import structlog

from twisted.internet import endpoints, reactor
from twisted.python import log
from twisted.web import server, wsgi

# CONTAINER
"""
this sets up everything that twisted needs in order to handle shutdowns as well as setting up a WSGI instance to interact with using twisted web (googlable).
"""
logger = logging.getLogger(__name__)
def run(app, address, debug):
    """Serve wsgi `app` on Twisted server endpoint `address`.

    :param app: wsgi application
    :param str address: twisted endpoint
    :param bool debug: enable debugging and reloading
    """

    def err_shutdown(failure):
        log.err(failure)
        reactor.callWhenRunning(reactor.stop)

    def _run():
        log.msg("logging run")
        # this is set in an oscar flag in pyg
        reactor.suggestThreadPoolSize(30) # this is the default in pyg.  Maybe we use something different.
        resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
        site = server.Site(resource)
        endpoint = endpoints.serverFromString(reactor, address)
        endpoint.listen(site).addErrback(err_shutdown)
        # this suggests that debug is boolean, perhaps
        reactor.run(installSignalHandlers=int(not debug))

    # this is a log event at the beginning of server init
    logger.info('event=\'starting twisted\' debug=%r address=%r',
                debug, address)

    if debug:
        import werkzeug.serving
        import werkzeug.debug
        app = werkzeug.debug.DebuggedApplication(app, evalex=True) # google me
        werkzeug.serving.run_with_reloader(_run)
    else:
        _run()

