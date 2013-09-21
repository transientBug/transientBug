#!/usr/bin/env python
"""
main index listing for gifs - reroutes to login if you're not logged in

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import config.config as c
import gevent

from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import login
from seshat.actions import Redirect

from utils.paginate import pager
import utils.files as fu


@login(["root"])
@autoRoute()
class index(HTMLObject):
    """
    Returns base index page listing all screenshots
    """
    _title = "screenshots"
    _defaultTmpl = "public/screenshots/index"
    def GET(self):
        """
        """
        self.view.data = {"header": "Screenshots"}

        perpage = self.request.getParam("perpage", 24)
        page = self.request.getParam("page", 0)
        sort_dir = self.request.getParam("dir", "desc")

        self.view.scripts = ["scrn"]

        f = []
        for top, folders, files in os.walk(c.general.dirs["screenshots"]):
            f.extend(files)
            break

        f, page_dict = pager(f, perpage, page, sort_dir)

        self.view.data = {"pictures": f, "page": page_dict}
        return self.view

    def POST(self):
        scrn = self.request.getFile("file")

        if scrn:
            path = ''.join([c.general.dirs["screenshots"], scrn.filename])
            try:
                fu.write_file(scrn, path)
                self.request.session.pushAlert("Screenshot is being uploaded...", level="success")
            except IOError as e:
                self.request.session.pushAlert("There was a problem executing \
                    that: {}".format(str(e)), level="error")

        return Redirect("/screenshots")
