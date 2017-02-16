# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_pygrap', [dirname(__file__)])
        except ImportError:
            import _pygrap
            return _pygrap
        if fp is not None:
            try:
                _mod = imp.load_module('_pygrap', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pygrap = swig_import_helper()
    del swig_import_helper
else:
    import _pygrap
del version_info
from _pygrap import *
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



























import sys
import os
import tempfile

def compute_tree(pattern_graphs):
    tree = ParcoursNode()

    n_patterns = 0
    max_site_size = 0
    for pattern_graph in pattern_graphs:
        added = tree.addGraphFromNode(pattern_graph, pattern_graph.root, pattern_graph.nodes.count, True)

        if added:
            n_patterns += 1
            if pattern_graph.nodes.count > max_site_size:
                max_site_size = pattern_graph.nodes.count
        else:
            sys.stderr.write("WARNING: One duplicate or incomplete pattern was not added.\n")

    return tree, max_site_size, n_patterns


def match_tree(tree, max_site_size, test_graph):
    rt = tree.parcourir(test_graph, max_site_size, True, True, False)

    pattern_matches = rt[1]
    return pattern_matches


def match_graph(pattern_arg, test_arg):
    if type(pattern_arg) is list:
        pattern_arg_list = pattern_arg
    else:
        pattern_arg_list = [pattern_arg]

    pattern_graph_list = []
    for pattern in pattern_arg_list:
        if isinstance(pattern, basestring):
            f = None
            if not os.path.isfile(pattern):
                f=tempfile.NamedTemporaryFile() 
                f.write(pattern)
                f.flush()
                pattern_path = f.name
            else:
                pattern_path = pattern

            pattern_graphs_ptr = getGraphListFromPath(pattern_path)
            pattern_graphs = MakeGraphList(pattern_graphs_ptr)

            if pattern_graphs is None or len(pattern_graphs) == 0:
                print("Pattern graph could not be opened or is empty.")
            else:
                pattern_graph_list += pattern_graphs

            if f is not None:
                f.close()
        else:
            pattern_graph_list.append(pattern)

    if isinstance(test_arg, basestring):
        test_graph = getGraphFromPath(test_arg)
    else:
        test_graph = test_arg

    if test_graph is None:
        print("Test graph could not be opened or is empty.")
        return None

    tree, max_site_size, n_patterns = compute_tree(pattern_graph_list)
    matches = match_tree(tree, max_site_size, test_graph)

    if isinstance(test_arg, basestring):
        freeGraphList(pattern_graphs_ptr, True, True)
    elif type(pattern_arg) is list:
        pass
    else:
        freeGraphList(pattern_graphs_ptr, True, True)

    return matches

# This file is compatible with both classic and new-style classes.


