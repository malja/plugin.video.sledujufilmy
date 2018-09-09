import urllib2
import cookielib
from bs4 import BeautifulSoup


def prepareUrlLib():
    """
    Prepare url opener for urllib.
    """
    # Prepare URL opener with Cookies
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)


def getHTML(url):
    """
    Return parsed HTML from URL. When connection fails, return None!
    :param url: URL of webpage to load.
    :return: BeaufifulSoup or None
    """

    # Parse HTML
    try:
        soup = BeautifulSoup(
            urllib2.urlopen(url),
            features="html.parser"
        )
    except IOError as e:
        return None

    return soup

