# -*- coding: utf-8 -*-

project = 'રાસ-ગરબા સંગ્રહ'
copyright = '2013-2019, P Adhia'
author = 'P Adhia'

version = '2019'
release = ''

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'

html_theme = "sphinx_rtd_theme"
html_theme_options = {'collapse_navigation': False, 'display_version': False}

def setup(app):
    app.add_stylesheet('css/rtd_override.css')

# html_theme = "alabaster"
# html_theme_options = {'fixed_sidebar': True}

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
html_static_path = ['_static']
html_logo = "_static/દાંડિયા.jpg"
html_favicon = "_static/favicon.ico"
