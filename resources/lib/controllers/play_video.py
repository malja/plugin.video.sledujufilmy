# -*- coding: utf-8 -*-
import xbmc

from resources.lib.router import Router
from resources.lib.scrappers import SledujuFilmy

@Router.register("/play-video")
def play_video(request):

    link = SledujuFilmy.resolveMovieLink(request.query("url"))
    xbmc.executebuiltin("PlayMedia(%s, False, 0)" % (link))