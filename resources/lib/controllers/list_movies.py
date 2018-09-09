# -*- coding: utf-8 -*-
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.router import Router
from resources.lib.scrappers import SledujuFilmy
from resources.lib.utils import buildUrl


@Router.register("/list_movies/latest")
def list_movies_latest(request):
    return _list_movies(
        request,
        SledujuFilmy.getLatest()
    )

@Router.register("/list_movies/category")
def list_movies_category(request):
    return _list_movies(
        request,
        SledujuFilmy.getCategoryMovies(request.query("category"), int(request.query("page"))),
        False,
        {
            "itemUrl": buildUrl(
                request.basePath(),
                {
                    "path": "/list_movies/category",
                    "page": int(request.query("page"))+1,
                    "category": request.query("category")
                }
            ),
            "itemLabel": xbmcaddon.Addon().getLocalizedString(30011),
        }
    )

def list_movies_search(request, name):

    movies = SledujuFilmy.search(name)
    if 0 == len(movies):
        # No search results
        xbmcgui.Dialog().ok(
            xbmcaddon.Addon().getLocalizedString(30012),
            xbmcaddon.Addon().getLocalizedString(30013),
        )
        return

    return _list_movies(
        request,
        movies
    )

def _list_movies(request, movies, sort = True, next = None):

    menu_items = []

    for movie in movies:

        item = xbmcgui.ListItem(
            label=movie["name"],
            iconImage=movie["image"],
            thumbnailImage=movie["image"],
            path=buildUrl(request.basePath(), {"path": "/select-source", "id": movie["id"]})
        )

        item.setInfo(
            "video",
            {
                "gendre": movie["gendres"],
                "country": movie["origin"],
                "year": movie["release"],
                "rating": movie["rating"],
                "playcount": movie["views"],
                "cast": movie["actors"],
                "plot": movie["description"],
                "mediatype": "movie"
            }
        )

        menu_items.append((
            buildUrl(request.basePath(), {"path": "/select-source", "id": movie["id"]}),
            item,
            False
        ))

    if next:
        menu_items.append((
            next["itemUrl"],
            xbmcgui.ListItem(
                label=next["itemLabel"],
                path=next["itemUrl"],
            ),
            True
        ))

    if 0 != len(menu_items):
        # Add all items at once - this should be faster than adding one by one.
        xbmcplugin.setContent(request.handle(), "movies")
        xbmcplugin.addDirectoryItems(request.handle(), menu_items)
        xbmcplugin.addSortMethod(request.handle(),
            xbmcplugin.SORT_METHOD_TITLE if sort else xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(request.handle(), succeeded=True)