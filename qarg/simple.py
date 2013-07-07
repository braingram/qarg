#!/usr/bin/env python

import sys


class ParseError(Exception):
    pass


class UnParseError(Exception):
    pass


def parse(arguments=None):
    """
    Simple argument parser

    Options
    ------

    arguments : arguments to parse
        if None, sys.argv[1:] will be used


    Returns
    ------

    args : list of strings
        arguments provided before options
            i.e. all arguments before the first '-something' argument

    opts : dictionary
        keys = parsed arguments (e.g. -k -> 'k', --key -> 'key')
        values = values of arguments
            True if present
            string if a value is provided (e.g. 'k': 'foo' if '-k foo')
            list of strings if multiple values are provided
                (e.g. 'k': ['foo', 'bar'] if '-k foo bar')
    """
    if arguments is None:
        arguments = sys.argv[1:]
    opts = {}
    k = None
    args = []
    for a in arguments:
        if len(a) == 0:
            continue
        if a[0] == '-':
            if a == '-':  # maybe this should 'reset' the key?
                raise ParseError("Invalid '-' argument: %s" % a)
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
                if k in opts:
                    if isinstance(opts[k], bool):
                        opts[k] = a
                    elif isinstance(opts[k], list):
                        opts[k].append(a)
                    else:
                        opts[k] = [opts[k], a]
                else:
                    opts[k] = a
    return args, opts


def key_to_opt(k):
    if len(k) == 1:
        return '-%s' % k
    return '--%s' % k


def unparse(args, opts):
    arguments = args[:]
    for k in opts:
        arguments.append(key_to_opt(k))
        if opts[k] is True:
            continue
        elif isinstance(opts[k], str):
            arguments.append(opts[k])
            continue
        elif isinstance(opts[k], (tuple, list)):
            arguments.extend(opts[k])
            continue
        raise UnParseError(
            "Invalid option type or value: %s: %s"
            % (k, opts[k]))
    return arguments


def test():
    assert key_to_opt('a') == '-a'
    assert key_to_opt('ab') == '--ab'

    args = 'a b c -x 1 -y -z 1 2 3 --foo --bar'.split()
    a, o = parse(args)
    assert len(a) == 3
    assert 'a' in a
    assert 'b' in a
    assert 'c' in a
    assert len(o) == 5
    assert 'x' in o
    assert 'y' in o
    assert 'z' in o
    assert 'foo' in o
    assert 'bar' in o
    assert o['x'] == '1'
    assert o['y'] is True
    assert o['z'] == ['1', '2', '3']
    assert o['foo'] is True
    assert o['bar'] is True

    ua = unparse(a, o)
    assert len(ua) == len(args)
    for a in args:
        assert a in ua
    for u in ua:
        assert u in args

    # check exceptions
    try:
        parse(['-'])
        assert False
    except ParseError:
        pass

    try:
        parse(['-aa'])
        assert False
    except ParseError:
        pass

    try:
        unparse([], {'a': 1})
        assert False
    except UnParseError:
        pass
