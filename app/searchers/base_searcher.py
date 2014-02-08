#!/usr/bin/env python
"""
Search all the things.
Just a general template for making more advanced searchers. This creates a
little bit of a nicer object to work with, I think, rather than the whoosh api.
Its also fully contained. A single searcher is all you need to both search and
index documents.

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import logging
import whoosh.qparser
import whoosh.writing
import whoosh.index
import whoosh.query

from whoosh.index import EmptyIndexError

import config.config as c

logger = logging.getLogger("search")


class BaseSearcher(object):
    def __init__(self, schema=None):
        if schema:
            self.set_schema(schema)

        self.get_index()

    def set_schema(self, schema):
        self._schema = schema

    def get_index(self):
        try:
            self.open_index()
        except (EmptyIndexError, OSError) as e:
            logger.exception(e)
            if self._schema is not None:
                self.create_index()
            else:
                raise Exception("No schema defined, and no index found.")

    def create_index(self):
        if not os.path.exists(c.dirs.search_index+self.name):
            os.makedirs(c.dirs.search_index+self.name)
        self.ix = whoosh.index.create_in(c.dirs.search_index+self.name, self._schema)

    def open_index(self):
        self.ix = whoosh.index.open_dir(c.dirs.search_index+self.name)

    def add(self, item):
        pass

    def add_multiple(self, items):
        for item in items:
            self.add(item)

    def update(self, item):
        pass

    def delete(self, id):
        document = whoosh.query.Term("id", id)
        self.writer.delete_by_query(document)

    def save(self):
        self.writer.commit()

    @property
    def writer(self):
        if not hasattr(self, "_writer") or not self._writer:
            self._writer = whoosh.writing.AsyncWriter(self.ix)
            #self._writer = self.ix.writer()

        return self._writer

    def search(self, search, limit=None):
        ids = []
        with self.ix.searcher() as searcher:
            if not isinstance(search, whoosh.qparser.QueryParser):
                query = whoosh.qparser.QueryParser("content", self.ix.schema).parse(search)
            else:
                query = search
            results = searcher.search(query, limit=limit)

            for item in results:
                ids.append(item["id"])

        return ids

    def count(self):
        return self.ix.doc_count()

    def __len__(self):
        return self.count()