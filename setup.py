#!/usr/bin/env python

from setuptools import setup, Extension

include_dirs = [
    'src/DASpec',
    '/home/dupu/Softwares/cmpfit/cmpfit-1.3a',   # add or remove path if necessary
]

library_dirs = [
    '/home/dupu/Softwares/cmpfit/cmpfit-1.3a',   # add or remove path if necessary
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
    version = '0.8',
    author = 'Pu Du', 
    description = """DASpec""", 
    ext_modules = [ext_swigDASpec, ext_carray], 
    py_modules = ["DASpec", "carray"],
)
