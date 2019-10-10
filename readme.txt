Dependency (please install them first):
1. GSL
2. swig
3. cmpfit 
(https://www.physics.wisc.edu/~craigm/idl/cmpfit.html)
4. pybwidget 
(https://sourceforge.net/projects/topographica/files/external-full-history/pybwidget-0.1.2_1.7.0.tar.gz/download)

Install:
1. run "python setup.py build_ext --inplace"
2. Add the path to your $PYTHONPATH
3. Add "DASpec_TEMPLATE_PATH" in .bashrc as the directory of template files, e.g., export $DASpec_TEMPLATE_PATH="..."

Usage:
1. run "DASpec_GUI.py" or "DASpec_GUI_4k.py" (for 4k screen) directly

2. DASpec_GUI.py -s spectrum_file.txt
% spectrum_file.txt has three columns: wavelength, flux, err:
4800.0    1.0e-15    1.0e-17
4801.0    1.1e-15    0.9e-17
4802.0    1.2e-15    1.0e-17
...

3. DASpec_GUI.py -b list.txt
% list.txt: 
spectrum_file1.txt
spectrum_file2.txt
spectrum_file3.txt
