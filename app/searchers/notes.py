#!/usr/bin/env python
"""
Search all the notes!

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

import searchers.base_searcher as searcher

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, DATETIME, BOOLEAN
from whoosh.analysis import FancyAnalyzer
from whoosh.qparser import QueryParser, MultifieldParser

import rethinkdb as r
from rethinkORM import RethinkCollection
import models.rethink.note.noteModel as nm

fields_to_search = ["title", "short_code", "contents", "tags"]


class NoteSchema(SchemaClass):
    id = ID(stored=True, unique=True)
    created = DATETIME()
    title = TEXT(analyzer=FancyAnalyzer(), spelling=True)
    contents = TEXT(spelling=True)
    public = BOOLEAN()
    draft = BOOLEAN()
    short_code = ID(stored=True, unique=True)
    disable = BOOLEAN()
    reported = BOOLEAN()
    tags = KEYWORD(commas=True)
    user = ID()


def get_note_data(note):
    d = {"id":unicode(note.id),
         "created":arrow.get(note.created).datetime,
         "title":unicode(note.title),
         "contents":unicode(note.contents),
         "public":note.public,
         "draft":note.draft,
         "short_code":unicode(note.short_code),
         "disable":note.disable,
         "reported":note.reported,
         "user":unicode(note.user)}

    if note.tags:
        d["tags"] = u",".join(note.tags)

    return d


class NoteSearcher(searcher.BaseSearcher):
    name = "notes"
    _schema = NoteSchema

    def add(self, note):
        d = get_note_data(note)

        self.writer.add_document(**d)

    def update(self, note):
        d = get_note_data(note)

        self.writer.update_document(**d)

    def search(self, search, limit=None, collection=False):
        """
        Returns a RethinkCollection containing all notes which matched the
        query contained in `search`
        """
        ids = []
        with self.ix.searcher() as searcher:
            if not isinstance(search, QueryParser):
                query = MultifieldParser(fields_to_search, self.ix.schema).parse(search)
            else:
                query = search
            results = searcher.search(query, limit=limit)

            for item in results:
                ids.append(item["id"])

        if collection and ids:
            query = r.table(nm.Note.table).get_all(*ids)
            results = RethinkCollection(nm.Note, query=query)

            return results

        return ids