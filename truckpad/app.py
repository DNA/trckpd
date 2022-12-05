import falcon.asgi
import logging

from .endpoints.drivers import Drivers 

class Base:
    async def on_get(self, req, res):
        res.media = {'hello': 'world'}

async def handle_uncaught_exception(req, resp, ex, params):
    logging.exception('Unhandled error')
    raise falcon.HTTPInternalServerError(title='App error')

def create_app():
    app = falcon.asgi.App()
    app.add_route('/', Base())
    app.add_route('/drivers', Drivers())
    app.add_error_handler(Exception, handle_uncaught_exception)

    return app

app = create_app()