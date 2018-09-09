import os
import sys
import urllib
from urlparse import parse_qs

import xbmc
import xbmcaddon

import StorageServer


class SettingsValue(object):
    """
    Contains value obtained from settings.
    """

    def __init__(self, name, value):
        """
        :param str name: Value name. It is not changeable later on.
        :param str value: Settings value.
        """
        self._name = name
        self._value = value.strip()

    def __str__(self):
        """
        Return value as string.
        :return: str
        """
        return self._value

    def __int__(self):
        """
        Return value as int or return 0 for non-integer values.
        :return: int
        """
        try:
            return int(self._value)
        except ValueError:
            return 0

    def __float__(self):
        """
        Return value as float or return 0 for non-float values.
        :return: float
        """
        try:
            return float(self._value)
        except ValueError:
            return 0.0

    def __bool__(self):
        """
        Return value as boolean.
        :return: bool
        """
        return self._value.lower() == "true"

    def setValue(self, value):
        """
        Set new value. You still have to save it by setting it back to `Settings` class!
        :param value: New value.
        """
        self._value = value


class Settings(object):
    """
    Class designed for accessing plugin configuration.
    """

    def __getattr__(self, name):
        raw_value = xbmcaddon.Addon().getSetting(name)

        if 0 == len(raw_value):
            raw_value = ""

        return SettingsValue(name, raw_value)

    def __setattr__(self, key, value):
        """
        Save value to settings.
        :param key: Setting name.
        :param value: New value. May be string or SettingsValue
        """
        xbmcaddon.Addon().setSetting(key, str(value))

    def showDialog(self):
        """
        Open dialog for user to change settings.
        """
        xbmcaddon.Addon().openSettings()


def getCacheServer(timeout = 24):
    """
    Return persistent cache for set timeout. After it, cache is cleared.
    :param int timeout: Number of hours for cache persistence
    :return: StorageServer
    """
    return StorageServer.StorageServer("plugin_video_sledujufilmy", timeout)


def buildUrl(base_path, data):
    """
    Create URL for links to other parts of this plugin.
    :param base_path: Path to plugin root.
    :param data: Additional data which is parsed into query string.
    :return: str
    """
    return base_path + "?" + urllib.urlencode(data)

def getMediaResource(resourceName):
    """
    Return full path to file located in directory `media` or empty string for non-existent file.
    :param str resourceName: Resource file name
    :return: str
    """

    path = os.path.join(
        xbmcaddon.Addon().getAddonInfo("path"),
        "resources",
        "media",
        resourceName
    )

    if os.path.exists(path):
        return path

    return ""

def parseQueryString():
    """
    Return query string as a dictionary.
    :return: dict
    """

    # Query string is received as the third command line argument
    query = parse_qs(sys.argv[2].lstrip("?"))

    newDict = {}
    for key, value in query.items():
        newDict[key] = value[0] if isinstance(value, list) else value

    return newDict

def showNotification(header, message):
    """
    Show informative notification.
    :param str header: Notification title
    :param str message: Notification text
    """
    xbmc.executebuiltin("Notification(%s, %s)" %(header, message))
