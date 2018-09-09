import xbmcaddon
from resources.lib.handler import LoggingHandler
from resources.lib import plugin

# Create new addon
xbmcaddon.Addon("plugin.video.sledujufilmy")

# Register LoggingHandler class as new handler for this addon
LoggingHandler.register()

# Run entry point to plugin
plugin.run()
