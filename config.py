#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
__license__   = 'GPL v3'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'


from PyQt5.Qt import QWidget, QHBoxLayout, QLabel, QLineEdit

from calibre.utils.config import JSONConfig

prefs = JSONConfig('plugins/CalibreBookBrainzPlugin')

# Set defaults
prefs.defaults['searchinbookbrainz'] = ''

class ConfigWidget(QWidget):

    def __init__(self):
        pass

    def save_settings(self):
        prefs['searchinbookbrainz'] = unicode(self.msg.text())

