#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
from calibre.customize import InterfaceActionBase

__license__ = 'GPL v3'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'


class CalibreBookBrainzInit(InterfaceActionBase):
    name = 'CalibreBookBrainzPlugin'
    description = 'Plugin for Calibre that allows you to query BookBrainz database'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Stanislaw Szczesniak'
    version = (0, 0, 1)
    minimum_calibre_version = (0, 0, 0)

    actual_plugin = 'calibre_plugins.CalibreBookBrainzPlugin.ui:Interface'

    def is_customizable(self):
        return False

    def config_widget(self):
        from calibre_plugins.CalibreBookBrainzPlugin.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        config_widget.save_settings()

        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
