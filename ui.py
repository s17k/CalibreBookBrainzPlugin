#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2015, Stanisław Szcześniak'
__docformat__ = 'restructuredtext en'

from calibre.gui2.actions import InterfaceAction
from calibre_plugins.CalibreBookBrainzPlugin.main import CalibreBookBrainzPluginDialog

class Interface(InterfaceAction):

    name = 'CalibreBookBrainzPlugin'
    action_spec = ('Book Brainz Search', None,
            'Query BB database', 'Ctrl+Shift+F1')

    def genesis(self):
        icon = get_icons('images/BB.svg')
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        # The base plugin object defined in __init__.py
        base_plugin_object = self.interface_action_base_plugin
        # Show the config dialog
        # The config dialog can also be shown from within
        # Preferences->Plugins, which is why the do_user_config
        # method is defined on the base plugin class
        do_user_config = base_plugin_object.do_user_config

        # self.gui is the main calibre GUI. It acts as the gateway to access
        # all the elements of the calibre user interface, it should also be the
        # parent of the dialog
        d = CalibreBookBrainzPluginDialog(self.gui, self.qaction.icon(), do_user_config)
        d.show()

    def apply_settings(self):
        from calibre_plugins.CalibreBookBrainzPlugin.config import prefs
        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        prefs

