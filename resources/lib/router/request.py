class KodiRequest(object):
    """
    This class is passed as first and only parameter to controller callbacks. It contains all information about Kodi
    request.
    """

    def __init__(self, addon_handle, base_path, query):
        self._handle = int(addon_handle)
        self._base_path = base_path
        self._query = query

    def handle(self):
        """
        Get addon handle - integer value received from Kodi.
        """
        return self._handle

    def basePath(self):
        """
        Get base path for addon.
        """
        return self._base_path

    def query(self, key=None, default=""):
        """
        Get query as python dict.
        """
        if key:
            if key in self._query:
                return self._query[key]
            else:
                return default

        return self._query
