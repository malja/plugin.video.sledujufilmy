from resources.lib.controllers.index import index
from resources.lib.controllers.categories import categories
from resources.lib.controllers.list_movies import list_movies_latest, list_movies_search, list_movies_category
from resources.lib.controllers.select_source import select_source
from resources.lib.controllers.play_video import play_video
from resources.lib.controllers.search import search

__ALL__ = [
    index, categories, list_movies_latest, list_movies_search, select_source, play_video, search, list_movies_category
]
