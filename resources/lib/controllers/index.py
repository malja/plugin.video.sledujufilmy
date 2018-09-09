# -*- coding: utf-8 -*-
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.router import Router, KodiRequest
from resources.lib.utils import buildUrl, getMediaResource


@Router.register("/")
def index(request):
    """
    Plugin main page. With list of all categories and search menu.
    :param KodiRequest request: Request data.
    """

    main_menu = [
        (
            buildUrl(request.basePath(), {"path": "/search"}),
            xbmcgui.ListItem(
                label=xbmcaddon.Addon().getLocalizedString(30009),
                iconImage=getMediaResource("search.png"),
                path=buildUrl(request.basePath(), {"path": "/search"})
            ),
            True
        ),
        (
            buildUrl(request.basePath(), {"path": "/categories"}),
            xbmcgui.ListItem(label=xbmcaddon.Addon().getLocalizedString(30014)),
            True
        ),
        (
            buildUrl(request.basePath(), {"path": "/list_movies/latest"}),
            xbmcgui.ListItem(label=xbmcaddon.Addon().getLocalizedString(30015)),
            True
        ),
    ]

    # Add all items at once - this should be faster than adding one by one.
    xbmcplugin.addDirectoryItems(request.handle(), main_menu)
    xbmcplugin.addSortMethod(request.handle(), xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(request.handle(), succeeded=True)
