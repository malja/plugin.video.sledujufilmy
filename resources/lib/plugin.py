# Import all controllers. This line is neccessary for working routing!
from resources.lib.controllers import *
from resources.lib.scrappers.common import prepareUrlLib
from resources.lib.router import Router


def run():
    """
    This is an entry point to plugin. It runs router, which (based on value in query string received from Kodi) decides
    which controller to run.
    """

    prepareUrlLib()
    Router.route()
