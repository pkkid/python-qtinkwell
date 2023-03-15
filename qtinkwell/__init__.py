# -*- coding: utf-8 -*-
import logging
import os
import sass
import sys
from os.path import dirname, normpath
from PySide6 import QtGui

VERSION = '1.0.0'
ROOT = dirname(__file__)
DEFAULT_STYLESHEET = normpath(f'{ROOT}/inkwell.sass')
DEFAULT_FONTDIR = normpath(f'{ROOT}/fonts')


# Custom logging formatter
class MyFormatter(logging.Formatter):
    def format(self, record):
        if 'module' in record.__dict__.keys():
            record.module = record.module[:10]
        return super(MyFormatter, self).format(record)


# Logging configuration
log = logging.getLogger(__name__)
logformat = MyFormatter('%(asctime)s %(module)10s:%(lineno)-4s %(levelname)-7s %(message)s')
streamhandler = logging.StreamHandler(sys.stdout)
streamhandler.setFormatter(logformat)
log.addHandler(streamhandler)
log.setLevel(logging.INFO)


def applyStyleSheet(qobj, filepath=DEFAULT_STYLESHEET, outline=False):
    """ Apply the specified stylesheet via libsass and add it to qobj. """
    styles = open(filepath).read()
    styles = sass.compile(string=styles)
    if outline:
        styles += 'QWidget { border:1px solid rgba(255,0,0,0.3) !important; }'
    qobj.setStyleSheet(styles)


def addApplicationFonts(dirpath=DEFAULT_FONTDIR):
    """ Load all ttf fonts from the specified dirpath. """
    for filename in os.listdir(dirpath):
        if filename.endswith('.ttf'):
            filepath = normpath(f'{dirpath}/{filename}')
            fontid = QtGui.QFontDatabase.addApplicationFont(filepath)
            fontname = QtGui.QFontDatabase.applicationFontFamilies(fontid)[0]
            log.info(f'Loading font {fontname}')