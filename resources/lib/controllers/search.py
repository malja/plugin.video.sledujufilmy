# -*- coding: utf-8 -*-
import xbmcgui
import xbmcaddon

from resources.lib.router import Router
from resources.lib.controllers import list_movies_search


@Router.register("/search")
def search(request):

    dialog = xbmcgui.Dialog()
    # Search
    movie_name = dialog.input(
        xbmcaddon.Addon().getLocalizedString(30009),
    )
    del dialog

    if 0 != len(movie_name):
        # Show "Searching..." dialog and search movies in background
        progress = xbmcgui.DialogProgress()
        # Searching, please wait
        progress.create(
            xbmcaddon.Addon().getLocalizedString(30002),
            xbmcaddon.Addon().getLocalizedString(30010)
        )
        progress.update(-1)
        list_movies_search(request, movie_name)
        progress.close()
        del progress
