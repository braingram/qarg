#!/usr/bin/env python

import sys


class ParseError(Exception):
    pass


def parse(arguments=None):
    if arguments is None:
        arguments = sys.argv[1:]
    opts = {}
    k = None
    args = []
    for a in arguments:
        if len(a) == 0:
            continue
        if a[0] == '-':
            if (len(a) > 1) and (a[1] == '-'):
                # long opt
                k = a[2:]
                opts[k] = True
            else:
                # short opt
                if len(a) != 2:
                    raise ParseError("Invalid short argument: %s" % a)
                k = a[1]
                opts[k] = True
        else:
            if k is None:
                args.append(a)
            else:
                if 'k' in opts:
                    if isinstance(opts[k], bool):
                        opts[k] = a
                    elif isinstance(opts[k], list):
                        opts[k].append(a)
                    else:
                        opts[k] = [opts[k], a]
                else:
                    opts[k] = a
    return args, opts
