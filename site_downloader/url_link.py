#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
UrlLink class for universal site downloader
Created 13.10.2016 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import re
from os.path import sep as os_path_sep

class UrlLink(object):
    HTML = 1
    CSS = 2
    JS = 3
    IMG = 4
    FONT = 5

    FORMATS = {
        1: 'html',
        2: 'css',
        3: 'js',
        4: ['jpg', 'jpeg', 'png', 'bmp', 'tga', 'gif', 'svg'],
        5: ['ttf', 'woff', 'eot', 'woff2'],
    }

    BIN_TYPES = [4, 5]

    DEFAULT_PATHES = {
        1: None,
        2: 'css',
        3: 'js',
        4: 'images',
        5: 'fonts'
    }

    def __init__(self, url, url_type, parent_url = 'NONE'):
        if isinstance(parent_url, UrlLink):
            parent_url = parent_url.normalized
        self.parent = parent_url
        self.url_path = parent_url.rsplit('/', 1)[0]
        self.type = url_type
        self.raw = url
        self.host = None
        self.protocol = None
        self.split_inst = None
        self.normalized = self.normalize_url()
        self.filename = self.to_filename()

    def __repr__(self):
        return '<{} (+) {} (->) {}>'.format(self.parent, self.raw, self.normalized)

    def __str__(self):
        return 'UrlLink(parent={x.parent}, raw={x.raw}, normalized={x.normalized}, type={x.type})'.format(x=self)

    def __eq__(self, other):
        if isinstance(other, UrlLink):
            return self.filename == other.filename
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.filename)

    def get_host(self):
        if self.host is None:
            self.host = re.match('(https?:)?//[^/]+', self.parent).group(0)
        return self.host

    def get_protocol(self):
        if self.protocol is None:
            self.protocol = re.match('https?:', self.parent).group(0)
        return self.protocol

    def super_url_join(self, *parts):
        """ joins parts and delets all useless substrings like this `/<something>/..` """
        result = '/'.join(parts)
        while 1:
            orig, result = result, re.sub('/[^./][^/]*/[.]{2}', '', result)
            if orig == result:
                break
        return result

    def normalize_url(self):
        if self.raw.startswith('http'):
            return self.raw
        elif self.raw.startswith('//'):
            return self.get_protocol() + self.raw

        elif self.raw.startswith('/'):
            if len(self.raw) == 1:
                return self.get_host()
            return self.get_host() + self.raw
        return self.super_url_join(self.url_path, self.raw)

    def clear(self):
        return re.split('[;#?]', self.normalized)[0]

    def transformed(self):
        return self.normalized.replace('?', '&')

    def to_filename(self):
        if self.type in self.BIN_TYPES:
            if '.' in self.clear():
                return self.clear()
            else:
                return self.transformed()
        else:
            filepath = self.transformed()
            rules = {x: '.' + self.FORMATS[x] for x in [self.HTML, self.JS, self.CSS]}
            if not filepath.endswith(rules[self.type]):
                filepath += rules[self.type]
        return filepath

    def split(self, start_part=None):
        """ 
            returns last url part if start_part is None or left peace after start part 
            this function also transforms all slashes to system separator (os.path.sep)
        """
        if self.split_inst is None:
            if start_part is None:
                self.split_inst = self.filename.rsplit('/', 1)[-1]
            else:
                self.split_inst = self.filename[len(start_part):].replace('/', os_path_sep)
        return self.split_inst

