import xbmcgui
import xbmcplugin
from resources.lib.router import Router
from resources.lib.scrappers import SledujuFilmy
from resources.lib.utils import buildUrl


@Router.register("/categories")
def categories(request):

    categories = SledujuFilmy.getCategories()

    # There should be saved all UI list before they are actually inserted into Kodi
    listOfCategories = []

    for category in categories:
        # Prepare list
        listOfCategories.append(
            (
                buildUrl(request.basePath(), {
                    "path": "/list_movies/category",
                    "page": 1,
                    "category": category["url"]
                }),
                xbmcgui.ListItem(label=category["name"]),
                True
            )
        )

    if 0 != len(listOfCategories):
        # Add all items at once - this should be faster than adding one by one.
        xbmcplugin.addDirectoryItems(request.handle(), listOfCategories)
        xbmcplugin.addSortMethod(request.handle(), xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.endOfDirectory(request.handle())
