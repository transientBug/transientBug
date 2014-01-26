#!/usr/bin/env python
"""
Utils for handling unsafe markdown
Renders and cleans

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import bleach as bl
import markdown as md

cleanTags = list(bl.ALLOWED_TAGS)
cleanTags.extend(['p', 'img', 'small', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','br', 'hr'])
cleanAttr = dict(bl.ALLOWED_ATTRIBUTES)
cleanAttr["img"] = ["src", "width", "height"]
cleanAttr["i"] = ["class"]


class CustomMarkdownExtension(md.Extension):
    def extendMarkdown(self, md, md_globals):
        pass


def sanitize(pre_clean):
    """
    Sanitize the input into safe HTML through bleach

    :param pre_clean: a `str` of (probably) html to sanitize
    """
    return bl.clean(pre_clean, tags=cleanTags, attributes=cleanAttr)


def markdown_raw(text):
    """
    Renders markdown into, well, markdown, through markdown2 and a custom
    markdown class (for custom preprocessing).

    These extras are enabled in markdown:
     * header-ids
     * footnote
     * fenced-code-blocks
     * break-on-newline
     * pyshell

    :param text: `str` or `unicode` object which is the text to render to html
    """
    extras = [
        "headerid",
        "footnotes",
        "fenced_code",
        "nl2br",
        "wikilinks",
        CustomMarkdownExtension()
    ]

    return md.markdown(text, extensions=extras)


def markdown(text):
    """
    Renders markdown into, well, markdown, through markdown2 and a custom
    markdown class (for custom preprocessing). Then runs it through bleach to
    sanitize it.

    These extras are enabled in markdown:
     * header-ids
     * footnote
     * fenced-code-blocks
     * break-on-newline
     * pyshell

    :param text: `str` or `unicode` object which is the text to render to html
    """
    text = markdown_raw(text)
    return sanitize(text)
