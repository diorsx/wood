#-*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import tempfile
import ConfigParser
from string import ascii_letters, digits

BOOL_TRUE = frozenset([ "true", "t", "y", "1", "yes", "on" ])

def mk_boolean(value):
    if value is None:
        return False
    val = str(value)
    if val.lower() in BOOL_TRUE:
        return True
    else:
        return False

def get_config(p, section, key, env_var, default, boolean=False):
    """get key-value, and then 
    """
    value = _get_config(p, section, key, env_var, default)
    if boolean:
        value = mk_boolean(value)
    return value

def _get_config(p, section, key, env_var, default):
    if env_var is not None:
        value = os.getenv(env_var, None)
        if value is not None:
            return value

    if p is not None:
        try:
            return p.get(section, key, raw=True)
        except:
            return default
    return default

def load_config_file():
    """按顺序加载配置文件,找到第一个可用的配置文件;
    顺序: ENV, CWD, HOME, /etc/wood
    """
    p = ConfigParser.ConfigParser()
    """get config file from env
    """
    path0 = os.getenv("WOOD_CONFIG", None)
    if path0 is not None:
        path0 = os.path.expanduser(path0)
        if os.path.isdir(path0):
            path0 += '/wood.cfg'
    
    """get config file from cwd
    """
    try:
        path1 = os.getcwd() + '/wood.cfg'
    except OSError:
        path1 = None

    path2 = os.path.expanduser("~/wood.cfg")
    path3 = r"/etc/wood/wood.cfg"

    """判断path是否存在，若存在,加载文件并解析"""
    for path in [path0, path1, path2, path3]:
        if path is not None and os.path.exists(path):
            p.read(path)
            return p, path
    return None, ''

p, path = load_config_file()
DEFAULT = 'default'

WOOD_FORCE_COLOR  = get_config(p, DEFAULT, 'force_color', 'WOOD_FORCE_COLOR', None, boolean=True)
WOOD_NOCOLOR      = get_config(p, DEFAULT, 'nocolor', 'WOOD_NOCOLOR', None, boolean=True)

COLOR_HIGHLIGHT   = get_config(p, 'colors', 'highlight', 'WOOD_COLOR_HIGHLIGHT', 'white')
COLOR_VERBOSE     = get_config(p, 'colors', 'verbose', 'WOOD_COLOR_VERBOSE', 'blue')
COLOR_WARN        = get_config(p, 'colors', 'warn', 'WOOD_COLOR_WARN', 'bright purple')
COLOR_ERROR       = get_config(p, 'colors', 'error', 'WOOD_COLOR_ERROR', 'red')
COLOR_DEBUG       = get_config(p, 'colors', 'debug', 'WOOD_COLOR_DEBUG', 'dark gray')
COLOR_DEPRECATE   = get_config(p, 'colors', 'deprecate', 'WOOD_COLOR_DEPRECATE', 'purple')
COLOR_SKIP        = get_config(p, 'colors', 'skip', 'WOOD_COLOR_SKIP', 'cyan')
COLOR_UNREACHABLE = get_config(p, 'colors', 'unreachable', 'WOOD_COLOR_UNREACHABLE', 'bright red')
COLOR_OK          = get_config(p, 'colors', 'ok', 'WOOD_COLOR_OK', 'green')
COLOR_CHANGED     = get_config(p, 'colors', 'changed', 'WOOD_COLOR_CHANGED', 'yellow')
COLOR_DIFF_ADD    = get_config(p, 'colors', 'diff_add', 'WOOD_COLOR_DIFF_ADD', 'green')
COLOR_DIFF_REMOVE = get_config(p, 'colors', 'diff_remove', 'WOOD_COLOR_DIFF_REMOVE', 'red')
COLOR_DIFF_LINES  = get_config(p, 'colors', 'diff_lines', 'WOOD_COLOR_DIFF_LINES', 'cyan')