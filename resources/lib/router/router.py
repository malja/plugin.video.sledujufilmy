import sys

from resources.lib.router.request import KodiRequest
from resources.lib.utils import parseQueryString


class Router(object):
    """
    Router takes command line arguments received from Kodi. It expects three parameters:
    1) Base path to plugin directory.
    2) Addon handle - numerical value used in some function calls.
    3) Query string - contains parameters for routing.
    Router is responsible for parsing query string and its key `path` respectively. When `path` is not set or there
    is no callback registered for it, function `index` is called. In other cases, corresponding callback is called
    with `KodiRequest` class as its first and only parameter.

    Each callback has to be registered. It's done with calling `Router.register` decorator. After all callbacks are
    registered, call `Router.route`.
    """

    routes = {}

    @staticmethod
    def register(route):
        """
        Decorator for registering new controller
        :param route: URL for which should be the controller executed
        :return: Controller
        """

        def register_wrapper(func):
            Router.routes[route] = func
            return func

        return register_wrapper

    @staticmethod
    def route():
        """
        Access command line arguments and select what function should be called based on `path` parameter in query
        string received from Kodi.
        When no callback is registered for `path`, function `index` is called.
        :return: Whatever returns the callback.
        """

        base_path = sys.argv[0]
        handle = sys.argv[1]
        query = parseQueryString()


        # Prepare request class
        request = KodiRequest(handle, base_path, query)

        if "path" not in query or query["path"] not in Router.routes:
            query["path"] = "/"

        # Call registered callback
        path = query["path"]
        func = Router.routes[path]
        return func(request)
