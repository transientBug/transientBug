"""
http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import arrow

from models.rethink.base_interface import BaseInterface
from models.validators.user_validator import UserValidator
from models.validators.tags_validator import TagsValidator
from models.validators.created_validator import CreatedValidator

import utils.markdown_utils as md
import utils.short_codes as sc


class Note(UserValidator, TagsValidator, CreatedValidator, BaseInterface):
    table = "notes"

    _user_field = "user"
    _tags_field = "tags"
    _created_field = "created"

    @classmethod
    def new_note(cls, user, title="", contents="", draft=True, public=False,
            toc=False, has_comments=False, tags=None, theme="default"):
        if not tags:
            tags = []

        time = arrow.utcnow()
        if not title:
            title = "Untitled Note @ %s" % time.format("YY/MM/DD HH:mm:ss")
        created = time.timestamp

        new_tags = [ tag.replace(" ", "_").lower() for tag in tags ]

        code = sc.generate_short_code(cls.table)

        what = cls.create(user=user,
                          created=created,
                          title=title,
                          contents=contents,
                          public=public,
                          tags=new_tags,
                          table_of_contents=toc,
                          draft=draft,
                          has_comments=has_comments,
                          short_code=code,
                          theme=theme,
                          disable=False,
                          reported=False)

        return what

    def copy(self, user):
        copy_data = self._data.copy().pop("id").pop("user")
        copy_data["short_code"] = sc.generate_short_code(self.table)
        copy_data["created"] = arrow.utcnow().timestamp
        copy_data["user"] = user.id

        copy = Note(**copy_data)

        return copy

    @property
    def contents(self):
        if not hasattr(self, "_formated_contents"):
            self._formated_contents = md.markdown(self._data["contents"])

        return self._formated_contents

    @contents.setter
    def contents(self, val):
        self._data["contents"] = val

    @property
    def raw(self):
        return self._data["contents"]

    def __json__(self):
        d = self._data.copy()
        d.pop("id")
        d.pop("theme")
        d.pop("disable")
        d.pop("reported")
        d["user"] = self.user.username

        return d
