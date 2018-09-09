# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.router import Router
from resources.lib.scrappers.common import getHTML
from resources.lib.scrappers.sledujufilmy import SledujuFilmy

@Router.register("/select-source")
def select_source(request):

    # Show informative dialog and get sources in background
    progress = xbmcgui.DialogProgress()
    # Searching, please stand by
    progress.create(
        xbmcaddon.Addon().getLocalizedString(30002),
        xbmcaddon.Addon().getLocalizedString(30003)
    )
    players_html = getHTML("http://stream-a-ams1xx2sfcdnvideo5269.cz/okno.php?movie=%s=&new_way" % (request.query("id")))
    progress.update(50)
    sources = SledujuFilmy.getMovieSources(players_html)
    progress.close()
    del progress

    if sources is None:
        # No sources, sorry
        xbmcgui.Dialog().notification(
            xbmcaddon.Addon().getLocalizedString(30017),
            xbmcaddon.Addon().getLocalizedString(30018),
        )
        return

    # Prepare source selection
    menu_items = []
    url_items = []
    for source in sources:
        menu_items.append(source["server"])
        url_items.append(source["source"])

    result = xbmcgui.Dialog().select(
        xbmcaddon.Addon().getLocalizedString(30004),
        menu_items
    )

    # Show informative dialog and resolve URL in background
    progress = xbmcgui.DialogProgress()
    # Contacting server, stand by
    progress.create(
        xbmcaddon.Addon().getLocalizedString(30005),
        xbmcaddon.Addon().getLocalizedString(30006)
    )
    resolved = SledujuFilmy.resolveMovieLink(url_items[result])
    progress.close()
    del progress

    if resolved:
        xbmc.executebuiltin("PlayMedia(%s, False, 0)" % (resolved))
    else:
        # Error, could not connect
        xbmcgui.Dialog().notification(
            xbmcaddon.Addon().getLocalizedString(30007),
            xbmcaddon.Addon().getLocalizedString(30008)
        )
