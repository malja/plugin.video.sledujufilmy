import logging

import xbmc
import xbmcaddon

from resources.lib.utils import Settings


class LoggingHandler(logging.StreamHandler):
    """
    Class which process logs from python logging into Kodi logs.
    """

    def __init__(self):
        """
        Create new stream handler.
        """

        logging.StreamHandler.__init__(self)
        formatter = logging.Formatter("[" + xbmcaddon.Addon().getAddonInfo('id') + "] - %(name)s %(message)s")
        self.setFormatter(formatter)

    def emit(self, record):
        """
        Proceed log message from python to Kodi.
        :param record: Error log.
        """

        # Match logging error levels with Kodi's
        levels = {
            logging.CRITICAL: xbmc.LOGFATAL,
            logging.ERROR: xbmc.LOGERROR,
            logging.WARNING: xbmc.LOGWARNING,
            logging.INFO: xbmc.LOGINFO,
            logging.DEBUG: xbmc.LOGDEBUG,
            logging.NOTSET: xbmc.LOGNONE,
        }

        if Settings().debug:
            xbmc.log(self.format(record).encode('utf-8', 'ignore'), levels[record.levelno])

    @staticmethod
    def register():
        """
        Register this class as logging handler
        """
        logger = logging.getLogger()
        logger.addHandler(LoggingHandler())
        logger.setLevel(logging.DEBUG)
