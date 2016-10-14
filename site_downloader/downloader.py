#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Universal site downloader
Created 12.10.2016 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import os
import re
import time
import requests
from multiprocessing.dummy import Pool as ThreadPool
from page import UrlPage
from url_link import UrlLink


class SiteDownloader(object):
    def __init__(self):
        self.logger = None
        self.chunk_size = 200
        self.errors = set()

    def set_logger(self, filename):
        self.logger = filename
        open(self.logger, 'w').write('')  # <---- erase old log info

    def log(self, text):
        """ Use it for log something. But it won't be work without logger setting (see set_logger method)."""
        if self.logger is not None:
            if text in self.errors:
                # this text has been already written
                return

            with open(self.logger, 'a') as f:
                self.errors.add(text)
                f.write(text + '\n')

    def set_root_level(self, root_url, root_path):
        self.root_path = root_path.replace('/', os.path.sep).replace('\\', os.path.sep)
        self.root_url = root_url
        if not root_url.endswith('/'):
            self.root_url += '/'

    def set_static_path(self, path):
        self.static_path = os.path.join(self.root_path, path)

    def get_filename_from_url(self, url):
        path = UrlLink.DEFAULT_PATHES[url.type]

        if path is not None:
            # This is static file
            return os.path.join(self.static_path, path, url.split())

        elif url.filename.startswith(self.root_url) and url.clear():
            # This is good HTML file
            return os.path.join(self.root_path, url.split(self.root_url))

        else:
            # This is HTML outside of root_url
            return '#'

    def get_relative_url(self, src, dst):
        src, dst = map(lambda x: self.get_filename_from_url(x).replace('\\', '/'), [src, dst])
        if dst == '#':
            return dst

        # Go back
        head, src_path = '', src.rsplit('/', 1)[0]
        while not dst.startswith(src_path):
            head += '../'
            src_path = os.path.split(src_path)[0]

        # Go dorward
        tail = dst[len(src_path):]
        if tail.startswith('/'):
            tail = tail[1:]

        return head + tail


    def save_page(self, url):
        """ saves single page with given url and returns new collected urls """
        filename = self.get_filename_from_url(url)

        if os.path.isfile(filename) or filename == '#':
            return []

        page = UrlPage(url)
        if page.invalid:
            self.log('Invalid page: {}'.format(str(url)))
            return []

        result = []
        for link in page.links():
            relpath = self.get_relative_url(url, link)
            page.replace_url(relpath)
            if relpath != '#':
                result.append(link)

        page.save(filename)
        self.collected += 1
        return result

    def save_pages(self, urls):
        """ saves multiple pages at once """
        urls = list(set(urls))
        new_urls = self.pool.map(self.save_page, urls)
        new_urls = sum(new_urls, [])
        self.urls += new_urls

    def download(self, initial_url, title='site', verbose=True):
        started_time = time.time()
        if verbose:
            print 'Collecting {}...'.format(title)

        self.urls = [UrlLink(initial_url, UrlLink.HTML)]
        self.collected = 0
        self.pool = ThreadPool(self.chunk_size)

        while self.urls:
            url_chunk = self.urls[:self.chunk_size]
            if verbose:
                print '\r[{}/{}] Saving {}...'.format(self.collected, len(self.urls), url_chunk[0].normalized),
            self.save_pages(url_chunk)
            del self.urls[:len(url_chunk)]

        if verbose:
            print '\nSite downloaded in {} seconds'.format(round(time.time() - started_time, 2))
