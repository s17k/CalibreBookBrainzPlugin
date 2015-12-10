#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'MIT'
__copyright__ = '2015 Stanislaw Szczesniak'
__docformat__ = 'restructuredtext en'

from PyQt5.Qt import QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel, QLineEdit, QListWidget, QListWidgetItem, QBrush, QColor, QPainter
import PyQt5.Qt
import requests

from calibre_plugins.CalibreBookBrainzPlugin.config import prefs

class DemoDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        # The current database shown in the GUI
        # db is an instance of the class LibraryDatabase from db/legacy.py
        # This class has many, many methods that allow you to do a lot of
        # things. For most purposes you should use db.new_api, which has
        # a much nicer interface from db/cache.py
        self.db = gui.current_db

        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.label = QLabel(prefs['searchinbookbrainz'])
        self.l.addWidget(self.label)

        self.setWindowTitle('Calibre Book Brainz Integration')
        self.setWindowIcon(icon)

        self.search_space =  QLineEdit()
        self.l.addWidget(self.search_space)

        self.listWidget = QListWidget()
        #for i in range(10):
        #    item = QListWidgetItem("Item %i" % i)
        #    self.listWidget.addItem(item)
        self.l.addWidget(self.listWidget)

        self.about_button = QPushButton('Search', self)
        self.about_button.clicked.connect(self.search)
        self.l.addWidget(self.about_button)




        #
        # self.marked_button = QPushButton(
        #     'Show books with only one format in the calibre GUI', self)
        # self.marked_button.clicked.connect(self.marked)
        # self.l.addWidget(self.marked_button)
        #
        # self.view_button = QPushButton(
        #     'View the most recently added book', self)
        # self.view_button.clicked.connect(self.view)
        # self.l.addWidget(self.view_button)
        #
        # self.update_metadata_button = QPushButton(
        #     'Update metadata in a book\'s files', self)
        # self.update_metadata_button.clicked.connect(self.update_metadata)
        # self.l.addWidget(self.update_metadata_button)
        #
        # self.conf_button = QPushButton(
        #         'Configure this plugin', self)
        # self.conf_button.clicked.connect(self.config)
        # self.l.addWidget(self.conf_button)
        #
        self.resize(400,600)

    def search(self):
        text=self.search_space.text()
        print(text)
        self.listWidget.clear()
        self.listWidget.setFocus()
        r = requests.get("https://bookbrainz.org/ws/search/?q=\"" + text + "\"&mode=\"search\"")
        hits = r.json()['hits']
        numQueries = len(hits)
        for i in range(numQueries) :
            item = QListWidgetItem("%i. %s" %((i+1),hits[i]['_source']['default_alias']['name']))
            Qcol = QColor()
            if i%2==0:
                Qcol.setRed(240)
                Qcol.setGreen(255)
                Qcol.setBlue(255)
            else :
                Qcol.setRed(220)
                Qcol.setGreen(255)
                Qcol.setBlue(240)
            item.setBackground(QBrush(Qcol))
            self.listWidget.addItem(item)

        self.listWidget.setFocus()


    def about(self):
        # Get the about text from a file inside the plugin zip file
        # The get_resources function is a builtin function defined for all your
        # plugin code. It loads files from the plugin zip file. It returns
        # the bytes from the specified file.
        #
        # Note that if you are loading more than one file, for performance, you
        # should pass a list of names to get_resources. In this case,
        # get_resources will return a dictionary mapping names to bytes. Names that
        # are not found in the zip file will not be in the returned dictionary.
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About the Calibre Book Brainz Plugin',
                text.decode('utf-8'))

    # def marked(self):
    #     ''' Show books with only one format '''
    #     db = self.db.new_api
    #     matched_ids = {book_id for book_id in db.all_book_ids() if len(db.formats(book_id)) == 1}
    #     # Mark the records with the matching ids
    #     # new_api does not know anything about marked books, so we use the full
    #     # db object
    #     self.db.set_marked_ids(matched_ids)
    #
    #     # Tell the GUI to search for all marked records
    #     self.gui.search.setEditText('marked:true')
    #     self.gui.search.do_search()
    #
    # def view(self):
    #     ''' View the most recently added book '''
    #     most_recent = most_recent_id = None
    #     db = self.db.new_api
    #     for book_id, timestamp in db.all_field_for('timestamp', db.all_book_ids()).iteritems():
    #         if most_recent is None or timestamp > most_recent:
    #             most_recent = timestamp
    #             most_recent_id = book_id
    #
    #     if most_recent_id is not None:
    #         # Get a reference to the View plugin
    #         view_plugin = self.gui.iactions['View']
    #         # Ask the view plugin to launch the viewer for row_number
    #         view_plugin._view_calibre_books([most_recent_id])

    # def update_metadata(self):
    #     '''
    #     Set the metadata in the files in the selected book's record to
    #     match the current metadata in the database.
    #     '''
    #     from calibre.ebooks.metadata.meta import set_metadata
    #     from calibre.gui2 import error_dialog, info_dialog
    #
    #     # Get currently selected books
    #     rows = self.gui.library_view.selectionModel().selectedRows()
    #     if not rows or len(rows) == 0:
    #         return error_dialog(self.gui, 'Cannot update metadata',
    #                          'No books selected', show=True)
    #     # Map the rows to book ids
    #     ids = list(map(self.gui.library_view.model().id, rows))
    #     db = self.db.new_api
    #     for book_id in ids:
    #         # Get the current metadata for this book from the db
    #         mi = db.get_metadata(book_id, get_cover=True, cover_as_data=True)
    #         fmts = db.formats(book_id)
    #         if not fmts:
    #             continue
    #         for fmt in fmts:
    #             fmt = fmt.lower()
    #             # Get a python file object for the format. This will be either
    #             # an in memory file or a temporary on disk file
    #             ffile = db.format(book_id, fmt, as_file=True)
    #             ffile.seek(0)
    #             # Set metadata in the format
    #             set_metadata(ffile, mi, fmt)
    #             ffile.seek(0)
    #             # Now replace the file in the calibre library with the updated
    #             # file. We dont use add_format_with_hooks as the hooks were
    #             # already run when the file was first added to calibre.
    #             db.add_format(book_id, fmt, ffile, run_hooks=False)
    #
    #     info_dialog(self, 'Updated files',
    #             'Updated the metadata in the files of %d book(s)'%len(ids),
    #             show=True)

    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        self.label.setText(prefs['hello_world_msg'])

