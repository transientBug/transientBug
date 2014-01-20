#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat_addons.mixed_object import MixedObject
from seshat_addons.func_mods import JSON

import models.utils.dbUtils as dbu
import models.rethink.phot.photModel as pm


@route()
class tags(MixedObject):
    @JSON
    def GET(self):
        base_query = dbu.rql_where_not(pm.Phot.table, "disable", True)

        raw_tags = base_query\
            .concat_map(lambda doc: doc["tags"])\
            .distinct()\
            .coerce_to('array').run()

        return {"tags": raw_tags}
