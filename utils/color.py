#-*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import sys

from wood import constants as C

WOOD_COLOR = True
if C.WOOD_NOCOLOR:
    WOOD_COLOR = False
elif not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
    WOOD_COLOR = False
else:
    try:
        import curses
        curses.setupterm()
        if curses.tigetnum('color') < 0:
            WOOD_COLOR = False
    except ImportError:
        pass
    except curses.error:
        WOOD_COLOR = False

if C.WOOD_FORCE_COLOR:
    WOOD_COLOR = True

codeCodes = {
    'black': u'0;30', 'bright gray': u'0;37',
    'blue': u'0;34', 'white': u'1;37',
    'green': u'0;32', 'bright blue': u'1;34',
    'cyan': u'0;36', 'bright green': u'1;32',
    'red': u'0;31', 'bright cyan': u'1;36',
    'purple': u'0;35', 'bright red': u'1;31',
    'yellow': u'0;33', 'bright purple': u'1;35',
    'dark gray': u'1;30', 'bright yellow': u'1;33',
    'magenta': u'0;35', 'bright magenta': u'1;35',
    'normal': u'0',
}

def parsecolor(color):
    """SGR parameter string for the specified color name."""
    matches = re.match(r"color(?P<color>[0-9]+)"
                       r"|(?P<rgb>rgb(?P<red>[0-5])(?P<green>[0-5])(?P<blue>[0-5]))"
                       r"|gray(?P<gray>[0-9]+)", color)
    if not matches:
        return codeCodes[color]
    if matches.group('color'):
        return u'38;5;%d' % int(matches.group('color'))
    if matches.group('rgb'):
        return u'38;5;%d' % (16 + 36 * int(matches.group('red')) +
                             6 * int(matches.group('green')) +
                             int(matches.group('blue')))
    if matches.group('gray'):
        return u'38;5;%d' % (232 + int(matches.group('gray')))

def stringc(text, color):
    """String in color."""
    if WOOD_COLOR:
        color_code = parsecolor(color)
        return u"\n".join([u"\033[%sm%s\033[0m" %(color_code, t) for t in text.split(u'\n')])
    else:
        return text