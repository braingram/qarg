#!/usr/bin/env python


import simple

try:
    from qargparse import get, parse
except ImportError as E:
    # I should import qoptparse here as a fallback
    # but... just reraise now
    raise E

__all__ = ['simple', 'get', 'parse']
