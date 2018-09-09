# -*- coding: utf-8 -*-
import xbmcaddon

import urlparse
import urllib

import urlresolver

from resources.lib.scrappers.common import getHTML
from resources.lib.utils import getCacheServer, Settings


class SledujuFilmy(object):

    URL = "https://sledujufilmy.cz"

    @staticmethod
    def getCategories():
        """
        Get all movie categories from the website. Cached version.

        **Format:**

            {
                "name": "Category name",
                "url": "Full link to category page",
            }

        :return: dict
        """

        cache = getCacheServer(
            int(Settings().cache_categories) * 24
        )

        return cache.cacheFunction(SledujuFilmy._get_categories)

    @staticmethod
    def _get_categories():
        """
        Get all movie categories from website.
        :return: dict
        """

        html = getHTML(SledujuFilmy.URL)

        # List of categories
        categories = []

        # Find all category links from home page
        if html:
            links = html.find(id="content").find(class_="genres").find_all("a")

            for link in links:
                if link.get("href"):
                    # And save them into list
                    categories.append({
                        "url": urlparse.urljoin(
                            SledujuFilmy.URL,
                            link["href"]
                        ),
                        "name": link.string
                    })

        return categories

    @staticmethod
    def getCategoryMovies(categoryUrl, page):
        """
        Get list of all movies from selected category and page. Cached version. See `_get_movies_from_list` for format.
        :param categoryUrl: Full link to category main page.
        :param page: Page number used for pagination.
        :return: dict
        """

        cache = getCacheServer(
            int(Settings().cache_movies)
        )
        return cache.cacheFunction(SledujuFilmy._get_category_movies, categoryUrl, page)

    @staticmethod
    def _get_category_movies(categoryUrl, page):
        """
        Get list of all movies from selected category and page. See `_get_movies_from_list` for format.
        :param categoryUrl: Full link to category main page.
        :param page: Page number used for pagination.
        :return: dict
        """
        html = getHTML(
            urlparse.urljoin(
                categoryUrl,
                "?" + urllib.urlencode({"pg": page}) if page > 1 else ""
            )
        )

        if html:
            category_movies = html.find(id="content").find(class_="riding-list").find_all("div", class_="item")
            return SledujuFilmy._get_movies_from_list(category_movies)

        return []

    @staticmethod
    def getLatest():
        """
        Get list of latest added movies. Cached version. See `_get_movies_from_list` for format.
        :return: list
        """

        # One day cache
        cache = getCacheServer(
            int(Settings().cache_movies)
        )
        return cache.cacheFunction(SledujuFilmy._get_latest)

    @staticmethod
    def _get_latest():
        """
        Get list of latest added movies. Cached version. See `_get_movies_from_list` for format.
        :return: list
        """

        html = getHTML(SledujuFilmy.URL)

        if html:
            latest_movies = html.find(id="content").find(class_="riding-list").find_all("div", class_="item")
            return SledujuFilmy._get_movies_from_list(latest_movies)

        return []

    @staticmethod
    def getMovieSources(html):
        """
        Return list of all available sources (streams) within given HTML. Cached version.

        **Format:**

            {
                "server": "Server name",
                "source": "Full link to source. It is not resolved to actual stream URL!"
            }

        :param html: HTML in which should it be searching for streams.
        :return: list
        """

        cache = getCacheServer(
            int(Settings().cache_movies)
        )
        return cache.cacheFunction(SledujuFilmy._get_movie_sources, html)

    @staticmethod
    def _get_movie_sources(html):
        """
        Return list of all available sources (streams) within given HTML. Cached version.

        **Format:**

            {
                "server": "Server name",
                "source": "Full link to source. It is not resolved to actual stream URL!"
            }

        :param html: HTML in which should it be searching for streams.
        :return: list
        """

        links = []
        for playerContainer in html.find_all("div", class_="player-container"):
            iframe = playerContainer.find("iframe")
            if iframe:

                server = urlparse.urlparse(iframe["src"])

                links.append({
                    "server": server.netloc,
                    "source": iframe["src"]
                })

        return links

    @staticmethod
    def resolveMovieLink(link):
        """
        Find actual link to stream from iframe or video URL. Or return False.

        This is necessary, because some streams would not be working if unresolved (that one you see in page source) URL
        URL is used.

        :param link: Unresolved link.
        :return: bool|str
        """
        return urlresolver.HostedMediaFile(url=link).resolve()

    @staticmethod
    def search(name):
        """
        Search movie by name. Cached version. Return empty array or list. See `_get_movies_from_list` for format.
        :param name: Movie name, or its part.
        :return: list
        """

        # One day cache
        cache = getCacheServer(
            int(Settings().cache_movies)
        )
        return cache.cacheFunction(SledujuFilmy._search, name)

    @staticmethod
    def _search(name):
        """
        Search movie by name. Return empty array or list. See `_get_movies_from_list` for format.
        :param name: Movie name, or its part.
        :return: list
        """
        html = getHTML(
            urlparse.urljoin(
                SledujuFilmy.URL,
                "vyhledavani/?" +
                urllib.urlencode({"search": name})
            )
        )

        if html:
            # Nothing was found for that search
            if html.find("div", class_="flash_message"):
                return []

            items = html.find("div", class_="mlist--list").find_all("div", class_="item")
            return SledujuFilmy._get_movies_from_list(items)

        return []

    @staticmethod
    def _get_movies_from_list(list):
        """
        Parse list of movies in HTML into PHP dictionary. On background, movie profile is visited for scrapping more
        information. This may take a while!

        **Format:**

            {
                "name": "Movie name",
                "description": "Long movie description (if found)",
                "rating": "CSFD rating from 0 to 10),
                "image": "Movie poster. Small size",
                "actors": "List of actors",
                "views": "Number of views on SledujuFilmy.cz",
                "length": "Length in minutes",
                "origin": "Country of movie origin",
                "release": "Release year",
                "gendres": "List of movie gendres",
                "id", "Movie ID for players scrappers. See getMovieSources()"
            }

        :param list: HTML with list of movies
        :return: dict
        """

        listOfMovies = []

        for movie in list:
            profile = getHTML(SledujuFilmy._get_movie_profile_url(movie))

            if profile:
                ratingText = profile.find("div", class_="rating").find("div", class_="csfd").contents[0].strip()
                rating = round(int(ratingText[:ratingText.find(" ") + 1]) / 10, 1)

                actors = SledujuFilmy._get_movie_actors(profile)
                data = SledujuFilmy._get_movie_data_chunks(profile)

                movieId = profile.find("div", id="play_block").find("a", class_="play-movie")["data-loc"]

                description = profile.find("p", id="movie_description").contents[1].string.strip()
                if "/" == description:
                    description = xbmcaddon.Addon().getLocalizedString(30001)

                listOfMovies.append({
                    "name": SledujuFilmy._get_movie_name(profile),
                    "description": description,
                    "rating": rating,
                    "image": SledujuFilmy._get_movie_icon(movie),
                    "actors": actors,
                    "views": int(profile.find("div", class_="rating").find("div", class_="views").find("div").string),
                    "length": data["length"] if data else "",
                    "origin": data["origin"] if data else "",
                    "release": data["release"] if data else "",
                    "gendres": data["gendres"] if data else "",
                    "id": movieId
                })

        return listOfMovies

    @staticmethod
    def _get_movie_profile_url(html):
        """
        Get link to the movie profile (where full information about movie is). Return empty string if not found.
        :param html: HTML in which to search.
        :return: str
        """
        try:
            return urlparse.urljoin(
                SledujuFilmy.URL,
                html.find("div", class_="ex").find("a", class_="view")["href"]
            )
        except AttributeError:
            return ""

    @staticmethod
    def _get_movie_icon(html):
        """
        Return movie poster link. SledujuFilmy uses small covers, it should be used as icon. Return empty string if not
        found.
        :param html: HTML in which to search
        :return: str
        """
        try:
            return urlparse.urljoin(
                SledujuFilmy.URL,
                html.find("div", class_="img--container").find("img")["src"]
            )
        except AttributeError:
            return ""

    @staticmethod
    def _get_movie_data_chunks(html):
        """
        Return additional information about movie. If not found, return None. In other cases, dict is returned.

        **Format:**

            {
                "release": "Release year",
                "origin": "Origin country name",
                "length": "Lengt in minutes",
                "gendres": "List of gendres"
            }

        :param html: HTML in which to search
        :return: None|dict
        """
        try:
            dataHtml = list(html.find("div", class_="info").find("div", class_="next").children)
        except AttributeError:
            return None

        data = ""
        for element in dataHtml:
            data += element.string.strip()

        parts = data.split("/")
        if 3 != len(parts):
            return None

        release = parts[0]
        release = int(release[release.find(":")+1:])

        origin = parts[1]
        origin = origin[origin.find(":")+1:]

        length,  gendres = parts[2].split(".")
        length = int(length[length.find(":")+1:length.find("m")])

        gendres = gendres.replace(" ", "").split(",")

        return {
            "release": release,
            "origin": origin,
            "length": length,
            "gendres": gendres
        }

    @staticmethod
    def _get_movie_actors(html):
        """
        Find movie cast in HTML and return it. If not found, returns empty array.
        :param html: HTML in which to search for the cast
        :return: list
        """
        try:
            actorLinks = html.find("div", class_="persons").find("div", class_="list scrolled").find_all("a")
        except AttributeError:
            return []

        actors = []
        for link in actorLinks:
            actors.append(link.string)

        return actors

    @staticmethod
    def _get_movie_name(html):
        """
        Find movie name in HTML and return it. If not found, returns "<Neznáný>".
        :param html: HTML in which to search for the name
        :return: str
        """
        try:
            names = html.find("div", class_="info").find("div", class_="names")
        except AttributeError:
            # "<Unknown>"
            return xbmcaddon.Addon().getLocalizedString(30000)

        return names.find("strong").string


