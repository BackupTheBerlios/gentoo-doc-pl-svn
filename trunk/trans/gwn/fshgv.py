#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable-msg=W0103
# Copyright 2005 Lukasz Strzygowski <lucass@gentoo.org> 
# Distributed under the terms of the GNU General Public License v2


"""
GuideXML to text converter
"""

import locale
import os
import re
import sys
import tempfile
import textwrap

from elementtree import ElementTree


class Parser(object):
    """Parser of GuideXML."""


    def make_title(self, title, length = 80, underline = None):
        """Wrap title to specified length and add optional underline."""

        title = title.strip()
        wrapped = textwrap.wrap(title, length)
        text = "\n".join(wrapped)

        if underline:
            maxlen = max(len(line) for line in wrapped)
            uline = underline * maxlen
            text = text + "\n" + uline

        return text
        
    def default_handler(self, node):
        """Default handler."""

        text = "".join(child[1] for child in self.iter_children(node))
        
        return text
        

    def handle_author(self, node):
        """Transform 'author' tags into:
        
        name <email> - title
        """
        
        title = node.attrib["title"]
        name = node[0].text
        mail = node[0].attrib["link"]
        
        text = "%s <%s> - %s" % (name, mail, title)

        return text

    
    def handle_guide(self, node):
        """Transform 'guide' tags into:
        
        title
        =====

        <chapters>

        <authors>
        """
        
        title = ""
        chapters = []
        authors = []

        for tag, value in self.iter_children(node):
            if tag == "abstract":
                title = value
            elif tag == "chapter":
                chapters.append(value)
            elif tag == "author":
                authors.append(value)
        
        title = self.make_title(title, 80, "=")
        chapters = "\n".join(chapters)
        authors = "\n".join(authors)
        

        text = "%s\n\n%s\n\nAutorzy:\n%s" % (title, chapters, authors)
        
        return text

        
    def handle_chapter(self, node):
        """Transform 'chapter' tags into:
        
        title
        -----
        
        <sections>
        """

        
        title = ""
        sections = []

        for tag, value in self.iter_children(node):
            if tag == "title":
                title = value
            elif tag == "section":
                sections.append(value)

        self.chapter_count += 1

        title = "%d. %s" % (self.chapter_count, title)
        title = self.make_title(title, 80, "-")
        sections = "\n".join(sections).lstrip()
            
        text = "\n%s\n\n%s" % (title, sections)

        
        return text


    def handle_pre(self, node):
        """Transform 'pre' tags into:
        
        .-----------.
        | <caption> |
        |-------------.
        | <some text> |
        `-------------'
        """

        caption = node.attrib["caption"]
        text = self.default_handler(node)

        row1 = ".%s." % ("-" * (len(caption) + 2))
        row2 = "| %s |" % caption
        
        lines = text.split("\n")[1:]
        lines = ["| %s" % line for line in lines]

        maxlen = max(len(line) for line in lines)
        if len(caption) > maxlen:
            maxlen = len(caption) + 2

        row3 = "|%s." % ("-" * maxlen)
        row4 = "`%s'" % ("-" * maxlen)
        
        lines = ["%s%s |" % (line, " " * (maxlen - len(line))) for line in lines]
        text = "\n".join(lines)

        text = "%s\n%s\n%s\n%s\n%s" % (row1, row2, row3, text, row4)
        
        return text
        
        
    def handle_section(self, node):
        """Transform 'section' tags into:

        title
        ^^^^^
        
        <body>

        <links>
        """

        title = ""
        body = ""
        links = []
        self.links = []

        
        for tag, value in self.iter_children(node):
            if tag == "title":
                title = value
            elif tag == "body":
                body = value

        for i, link in enumerate(self.links):
            number = i + self.link_count + 1
            prefix = " %d. " % number
            indent = len(prefix)
            wrapped = textwrap.wrap(link, 80 - indent)
            mylink = prefix + ("\n%s" % (" " * indent)).join(wrapped)
            links.append(mylink)

        self.link_count += len(self.links)

        text = body

        if title:
            title = self.make_title(title, 80, "^")
            text = "\n%s\n\n%s" % (title, text)

        if links:
            links = "\n".join(links)
            text = "%s\n\n%s" % (text, links)
    
        return text
        

    def handle_body(self, node):
        """Transform 'body' tags into wrapped text."""

        
        text = ""

        notwrapped = ("pre", "table", "ul", "ol")
        
        for tag, value in self.iter_children(node):
            if not value.strip():
                continue

            if tag in notwrapped:
                text = "%s\n\n%s" % (text, value)
            else:
                wrapped = textwrap.wrap(value, 80)
                text = "%s\n\n%s" % (text, "\n".join(wrapped))
                
        text = text[2:]
        
        return text

        
    def handle_warn(self, node):
        """Transform 'warn' tags into:

        Ostrzeżenie: <text>
        """

        text = "Ostrzeżenie: %s" % self.default_handler(node)

        return text

        
    def handle_note(self, node):
        """Transform 'note' tags into:

        Uwaga: <text>
        """

        text = "Uwaga: %s" % self.default_handler(node)

        return text

    def handle_comment(self, node):
        """Transform 'comment' tags into:

        (<text>)
        """

        text = "(%s)" % self.default_handler(node)

        return text
        
        
    def handle_mail(self, node):
        """Transform 'mail' tags into:

        <text>[<number>]
        
        Link will be inserted in a list after current section.
        """
        
        if "link" in node.attrib:
            link = node.attrib["link"]
            self.links.append(link)
            number = self.link_count + len(self.links)
            text = "%s[%d]" % (node.text, number)
        else:
            text = node.text

        return text
        

    def handle_figure(self, node):
        """Transform 'figure' tags into:

        Ilustracja[<number>]: <caption>
        
        Link will be inserted in a list after current section.
        """

        link = node.attrib["link"]
        if link[0] == "/":
            link = "http://gentoo.org%s" % link
        self.links.append(link)
    
        number = self.link_count + len(self.links)
        caption = node.attrib["caption"]
        
        text = "Ilustracja[%d]: %s" % (number, caption)
        
        return text

        
    def handle_ul(self, node):
        """Transform 'ul' tags into:

         * <li>
         * <li>
        """
        
        items = []
        
        for tag, value in self.iter_children(node):
            if tag != "li":
                continue
            wrapped = textwrap.wrap(value.strip(), 80-3)
            item = "\n   ".join(wrapped)
            items.append(item)

        text = " * %s" % "\n * ".join(items)
            
        return text

    
    def handle_ol(self, node):
        """Transform 'ol' tags into:

         1. <li>
         2. <li>
        """
        
        text = ""
        i = 0
        for tag, value in self.iter_children(node):
            if tag != "li":
                continue
            i = i + 1
            prefix = " %d. " % i
            wrapped = textwrap.wrap(value.strip(), 80 - len(prefix))
            item = ("\n%s" % (" "*len(prefix))).join(wrapped)
            text += "\n%s%s" % (prefix, item)
            
        return text
        
        
    def handle_p(self, node):
        """Transform 'p' tags with default handler and strip them."""

        text = self.default_handler(node).strip()
    
        return text
    
    
    def handle_uri(self, node):
        """Transform 'uri' tags into:

        <text>[<number>]

        Link will be inserted in a list after current section.
        """
        
        link = node.attrib["link"]
        
        if link[0] == "/":
            link = "http://gentoo.org%s" % link
            
        
        # if link refers to the same document, we just ignore it
        if link[0] != "#":
            self.links.append(link)
            number = self.link_count + len(self.links)
            text = "%s[%d]" % (node.text, number)

        else:
            text = node.text
            
        return text
    
        
    def iter_children(self, node):
        """Iterate over node's children and run appropriate handlers."""
        
        handlers = { \
            "author": self.handle_author,
            "body": self.handle_body,
            "chapter": self.handle_chapter,
            "comment": self.handle_comment,
            "figure": self.handle_figure,
            "guide": self.handle_guide,
            "mail": self.handle_mail,
            "note": self.handle_note,
            "ol": self.handle_ol,
            "p": self.handle_p,
            "pre": self.handle_pre,
            "section": self.handle_section,
            "ul": self.handle_ul,
            "uri": self.handle_uri,
            "warn": self.handle_warn,
        }

        skipped = ("date", "subtitle", "summary", "version")
            
        if node.text:
            yield "TEXT", node.text
           
        for child in node:
            tag = child.tag
            
            if tag in handlers:
                retval = handlers[tag](child)

            elif tag in skipped:
                retval = ""

            else:
                retval = self.default_handler(child)
                
            yield tag, retval
        
            if child.tail:
                yield "TEXT", child.tail


    def parse(self, path):
        """Parse specified document and return it's textual representation."""
        
        tree = ElementTree.parse(path)
        root = tree.getroot()
        text = self.handle_guide(root)

        return text
        

    def __init__(self):
        """Initialize."""
        
        self.chapter_count = 0
        self.link_count = 0
        self.links = []

        

def _preprocess(srcpath, dstpath):
    """Remove from document unnecessary whitespaces and
    save under other name in order to make parsing easier.
    """
    
    text = file(srcpath).read()
    pre = re.compile("<pre *(.*?)</pre>", re.DOTALL)

    all_pres = pre.findall(text)

    for i, pre in enumerate(all_pres):
        text = text.replace(pre, "\a%d\a" % i)

    text = re.sub("\n\s*</", "</", text)
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    while "  " in text:
        text = text.replace("  ", " ")

    for i, pre in enumerate(all_pres):
        text = re.sub("\a%d\a" % i, pre.strip(), text)

    file(dstpath, "w").write(text)
        


def run(argv = sys.argv):
    """Run fshgv."""
    
    if len(argv) < 2:
        sys.exit("Usage: %s [newsletter.xml]" % __file__)

    reload(sys)
    sys.setdefaultencoding("utf-8")
    
    srcpath = argv[1]
    
    tmpfd, tmppath = tempfile.mkstemp(suffix = "fshgv", text = True)
    os.close(tmpfd)

    _preprocess(srcpath, tmppath)

    parser = Parser()

    textual = parser.parse(tmppath)
    os.unlink(tmppath)    
    
    textual = textual.encode(locale.getpreferredencoding(), "ignore")
    
    print textual

        
if __name__ == "__main__":
    run()
