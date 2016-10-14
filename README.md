# SiteDownloader
This project is a micro pyhon2.7 module for site downloading. It can be used for downloading small sites. If you haven't internet or your internet connection is very slow you can use this module to download some site (or part of site) on other computer or place for your personal use.

This module uses only one not built-in library - [requests]

[requests]: http://docs.python-requests.org/en/master/

## Project Setup
To download site you can follow this instructions:

### Instructions
  1. Clone the template project, replacing some strings in main.py:
  
    ```
    git clone https://github.com/Alick09/SiteDownloader.git my-project
    cd my-project
    ```
   
  2. Install requests if you not installed it yet:
  
    ```
    pip install requests
    ```
   
  3. Edit the `my-project/main.py` file
  
  4. Run program:
  
    ```
    python main.py
    ```
  
### Editing `main.py`
  
  ```python
  from site_downloader import SiteDownloader
  sd = SiteDownloader()
  sd.set_logger('log.txt')
  sd.set_root_level('http://site.ru/somepath/', 'site')
  sd.set_static_path('static')
  sd.download('http://site.ru/somepath/index.php', title='site_title')
  ```
  
  * Method `set_logger` uses for log different errors, warnings or other useful information.
    If you will remove this line, log file won't be created.
    
  * Method `set_root_level` takes two params `url_root`, `file_root_path` it's need to get not all site, but only part (`http://site.ru/somepath/*` by example). See table below for better understanding this method.
  
  * Method `set_static_path` takes one parameter - path relative to `file_root_path`. All static files (images, styles, js, fonts) will be saved there.
  
  * Method `download` takes next parameters:
    * `initial_url` - url will be used to search other urls.
    * `title` (optional) - title for writing logs to console.
    * `verbose` (optional) - False for silent mode.
  
  * Table shows how different pages will be saved on you project path (by the example above):
    
    | page type     | url           | save path  |
    | ------------- |---------------| ------|
    | html          | `http://site.ru/somepath/index.html` | site/index.html |
    | html      | `http://site.ru/somepath/foo/index.html` | site/foo/index.html |
    | js | `http://site.ru/js/file.js`   | site/static/js/file.js |
    | js | `http://site.ru/foo/bar/js/other_file.js`   | site/static/js/other_file.js |
    | img | `http://other_site.com/files/img/image.png` | site/static/images/image.png |
    
### Development
  This modules not works with static files collision, with "not-affecting" parameters in links and some other features.
  
  But if you want to make this project better, you can help suggesting your fixes and changes.
  
  
