# -*- coding: utf-8 -*-

# At the bottom of conf.py
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)

import recommonmark
from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'PGConfig API'
copyright = u'2016, Sebastian Webber and contributors'
author = u'Sebastian Webber and contributors'

github_doc_root = 'https://github.com/sebastianwebber/pgconfig-api/tree/master/docs'
