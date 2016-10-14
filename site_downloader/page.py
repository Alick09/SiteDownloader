#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Page class for universal site downloader
Created 12.10.2016 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import os, requests, re
from url_link import UrlLink


def ag_mkdir(path):
    if not os.path.isdir(path):
        parent_path, folder = os.path.split(path)
        if not folder:
            raise RuntimeError("Disk {} doesn't exists".format(parent_path))
        if parent_path:
            ag_mkdir(parent_path)
        os.mkdir(path)


class UrlPage(object):
    def __init__(self, url):
        self.url = url
        try:
            self.request = requests.get(url.normalized)
            self.content = self.request.content
            self.new_content = self.content
            self.invalid = False
        except:
            self.invalid = True

    def save(self, savepath):
        folder = os.path.split(savepath)[0]
        if folder:
            ag_mkdir(folder)
        open_type = 'wb' if self.url.type in UrlLink.BIN_TYPES else 'w'
        with open(savepath, open_type) as f:
            f.write(self.new_content)

    def replace_url(self, url):
        self.replace_with = url

    def html_links(self):
        url_regexp = re.compile(r'<(a|link)\s+[^>]*?href=[\'"]([^\'"]+)[\'"]|<(script|img)\s+[^>]*?src=[\'"]([^\'"]+)[\'"]')
        type_mapper = {'a': UrlLink.HTML, 'link': UrlLink.CSS, 'script': UrlLink.JS, 'img': UrlLink.IMG}

        for url_match in url_regexp.finditer(self.content):
            shift = 2 if url_match.group(1) is None else 0
            urltype, url = type_mapper[url_match.group(shift + 1)], url_match.group(shift + 2)
            start, end = map(max, [[url_match.start(x) for x in [2, 4]],[url_match.end(x) for x in [2, 4]]])

            if url.startswith('mailto:') or url=='#':
                continue

            yield UrlLink(url, urltype, parent_url=self.url), (start, end)

    def css_links(self):
        url_regexp = re.compile(r'url\s*\(\s*[\'"]?\s*([^)\'"]+)\s*[\'"]\s*\)')

        for url_match in url_regexp.finditer(self.content):
            clear = UrlLink(url_match.group(1), UrlLink.IMG, parent_url=self.url).clear()
            file_format = clear.rsplit('.', 1)[-1].lower()
            if file_format in UrlLink.FORMATS[UrlLink.IMG]:
                yield UrlLink(url_match.group(1), UrlLink.IMG, parent_url=self.url), (url_match.start(1), url_match.end(1))
            elif file_format in UrlLink.FORMATS[UrlLink.FONT]:
                yield UrlLink(url_match.group(1), UrlLink.FONT, parent_url=self.url), (url_match.start(1), url_match.end(1))
            else:
                print '\nUnknown format: ' + file_format + ' (in {})'.format(self.url)
                continue

    def js_links(self):
        raise StopIteration()

    def links(self):
        """
            All links generators must only yield tuples with 2 elements:
                url - UrlLink
                rep_bounds - tuple with two integers: start and end pos of url string,

        """
        self.new_content, self.last_pos = '', 0
        if self.url.type not in UrlLink.BIN_TYPES:
            gen = {
                UrlLink.HTML: self.html_links, 
                UrlLink.CSS: self.css_links, 
                UrlLink.JS: self.js_links
            }[self.url.type]
            for url, rep_bounds in gen():
                self.new_content += self.content[self.last_pos:rep_bounds[0]]
                self.replace_with, self.last_pos = url, rep_bounds[1]
                yield url
                self.new_content += self.replace_with

        self.new_content += self.content[self.last_pos:]
