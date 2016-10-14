from site_downloader import SiteDownloader
sd = SiteDownloader()
sd.set_logger('log.txt')
sd.set_root_level('http://site.ru/somepath/', 'site')
sd.set_static_path('static')
sd.download('http://site.ru/', title='ag-one')