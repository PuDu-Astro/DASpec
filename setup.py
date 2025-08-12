#!/usr/bin/env python

from setuptools import setup, Extension

include_dirs = [
    'src/DASpec',
    '/Users/dupu/Softwares/cmpfit',             # add or remove path if necessary
    '/opt/homebrew/include',                    # add or remove path if necessary
]

library_dirs = [
    '/Users/dupu/Softwares/cmpfit',             # add or remove path if necessary
    '/opt/homebrew/lib',                        # add or remove path if necessary
]

ext_swigDASpec = Extension(
    name = '_swigDASpec',
    swig_opts = ['-c++'],
    sources = [
        'compcontainer.cpp',
        'component.cpp',
        'curvefit.cpp',
        'function.cpp',
        'swigDASpec.i',
    ],
    include_dirs = include_dirs,
    library_dirs = library_dirs,
    extra_compile_args = [
        '-fPIC',
        ],
    extra_link_args = [
        '-lmpfit',
        '-lgsl',
        '-lgslcblas',
    ]
)

ext_carray = Extension(
    name = '_carray',
    swig_opts = ['-c++'],
    sources = [
        'carray.cpp', 
        'carray.i',
    ],
    include_dirs = include_dirs
)

setup(
    name = 'DASpec',
    version = '0.9',
    author = 'Pu Du', 
    description = """DASpec""", 
    ext_modules = [ext_swigDASpec, ext_carray], 
    py_modules = ["DASpec", "carray"],
)
