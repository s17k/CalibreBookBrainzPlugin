#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'

from PyQt5.Qt import QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel, QLineEdit, QListWidget, QListWidgetItem, \
    QBrush, QColor, QPixmap
import PyQt5.Qt
import json
import urllib2


def request_get(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data


from calibre_plugins.CalibreBookBrainzPlugin.config import prefs


class CalibreBookBrainzPluginDialog(QDialog):
    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        self.db = gui.current_db

        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.header = QLabel(prefs['searchinbookbrainz'])
        self.l.addWidget(self.header)

        self.img = QLabel()
        pixmap = QPixmap("images/BBt.svg")
        self.img.setPixmap(pixmap)
        self.l.addWidget(self.img)

        # QCol = QColor()
        # QCol.setRed(220)
        # QCol.setGreen(255)
        # QCol.setBlue(240)


        self.setWindowTitle('Calibre Book Brainz Integration')
        self.setWindowIcon(icon)

        self.search_space = QLineEdit()
        self.selected_button = QPushButton('Use title from selected book', self)
        self.selected_button.clicked.connect(self.exporttitlefromselected)
        self.l.addWidget(self.selected_button)

        self.search_space = QLineEdit()
        self.l.addWidget(self.search_space)

        self.listWidget = QListWidget()
        self.l.addWidget(self.listWidget)

        self.searchExecutionButton = QPushButton('Search', self)
        self.searchExecutionButton.clicked.connect(self.search)
        self.l.addWidget(self.searchExecutionButton)

        self.aboutButton = QPushButton('About', self)
        self.aboutButton.clicked.connect(self.about)
        self.l.addWidget(self.aboutButton)

        self.resize(400, 600)
        self.search_space.setFocus()

    def exporttitlefromselected(self):
        rows = self.gui.current_view().selectionModel().selectedRows()
        if len(rows) == 0:
            self.search_space.setText("")
        else:
            mi = self.gui.library_view.model().db.get_metadata(rows[0].row())
            self.search_space.setText(mi.title)

    def search(self):

        text = self.search_space.text()
        print(text)
        self.listWidget.clear()
        self.listWidget.setFocus()
        try:
            url = "https://bookbrainz.org/ws/search/?q=\"" + text + "\"&mode=\"search\""
            hits = request_get(url)['hits']
        except:
            return
        numQueries = len(hits)
        act = 0
        for i in range(numQueries):
            enttype = hits[i]['_source']['_type']
            if not enttype in ['Publication', 'Work', 'Edition']:
                continue
            print(hits[i])
            item = QListWidgetItem("%i. %s BBID : %i" % ((act + 1), hits[i]['_source']['default_alias']['name'], 1))
            Qcol = QColor()
            if i % 2 == 0:
                Qcol.setRed(240)
                Qcol.setGreen(255)
                Qcol.setBlue(255)
            else:
                Qcol.setRed(220)
                Qcol.setGreen(255)
                Qcol.setBlue(240)
            item.setBackground(QBrush(Qcol))
            self.listWidget.addItem(item)
            act += 1

        self.listWidget.setFocus()
        self.searchExecutionButton.setFocus()

    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About the Calibre Book Brainz Plugin',
                          text.decode('utf-8'))

    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        self.label.setText(prefs['hello_world_msg'])
