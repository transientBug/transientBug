#!/usr/bin/env python
"""
main index listing for notes - reroutes to login if you're not logged in

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat_addons.seshat.mixed_object import MixedObject
from seshat_addons.seshat.obj_mods import template
from seshat_addons.seshat.func_mods import HTML

from utils.paginate import Paginate

from searchers.phots import PhotSearcher

import models.rethink.phot.photModel as pm
import models.utils.dbUtils as dbu


@route()
@template("public/phots/search/index", "Phots Search")
class search(MixedObject):
    @HTML
    def GET(self):
        q = dbu.rql_where_not(pm.Phot.table, "disable", True)

        all_tags = q\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        self.view.data = {"tags": all_tags, "phot_page": None}

        search_term = self.request.get_param("s")
        if search_term:
            search_term = search_term.replace("tag:", "tags:")

            searcher = PhotSearcher()
            phots_hidden_filter = dbu.rql_where_not(pm.Phot.table, "disable", True, raw=True)
            ids = searcher.search(search_term, collection=True, pre_filter=phots_hidden_filter)

            if ids is not None:
                ids.fetch()

                page = Paginate(ids, self.request, "title", sort_direction_default="desc")
                self.view.data = {"phot_page": page}

            self.view.template = "public/phots/search/results"

        return self.view
