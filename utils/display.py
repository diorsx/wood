#-*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import errno
import textwrap

import fcntl
from struct import unpack, pack
from termios import TIOCGWINSZ
from wood import constants as C

from wood.utils.color import stringc

class Display(object):
    """docstring for Display"""
    def __init__(self, verbosity=0):
        super(Display, self).__init__()
        self.columns = None
        self.verbosity = verbosity
        self._set_column_width()

    def display(self, msg, color=None, stderr=None):

        nocolor = msg
        if color:
            msg = stringc(msg, color)
        
        if not msg.endswith(u"\n"):
            msg2 = msg + u"\n"
        else:
            msg2 = msg

        if not stderr:
            fileobj = sys.stdout
        else:
            fileobj = sys.stderr

        fileobj.write(msg2)
        try:
            fileobj.flush()
        except IOError as e:
            if e.error != errno.EPIPE:
                raise

    def warning(self, msg, formatted=False):

        if not formatted:
            new_msg = "[WARNING]: %s" % msg
            wrapped = textwrap.wrap(new_msg, width=self.columns)
            new_msg = "\n".join(wrapped) + "\n"
        else:
            new_msg = "[WARNING]: %s" % msg

        self.display(new_msg, color=C.COLOR_WARN, stderr=True)


    def error(self, msg, wrap_text=True):
        if wrap_text:
            new_msg = u"[ERROR]: %s" % msg
            wrapped = textwrap.wrap(new_msg, width=self.columns)
            new_msg = u"\n".join(wrapped) + u"\n"
        else:
            new_msg = u"[ERROR]: %s" % msg

        self.display(new_msg, color=C.COLOR_ERROR, stderr=True)

    def info(self, msg, wrap_text=True):
        if wrap_text:
            new_msg = u"[INFO]: %s" % msg
            wrapped = textwrap.wrap(new_msg, width=self.columns)
            new_msg = u"\n".join(wrapped) + u"\n"
        else:
            new_msg = u"[INFO]: %s" % msg

        self.display(new_msg, color=C.COLOR_OK)

    def _set_column_width(self):
        if os.isatty(0):
            tty_size = unpack('HHHH', fcntl.ioctl(0, TIOCGWINSZ, pack('HHHH', 0, 0, 0, 0)))[1]
        else:
            tty_size = 0
        self.columns = max(79, tty_size - 1)