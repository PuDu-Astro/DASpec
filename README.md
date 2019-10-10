# DASpec
## Decomposition of AGN Spectrum (DASpec)
A multi-component spectral fitting code for active galactic nuclei with GUI interface

Version: 0.8

Author: Pu Du

### Dependency (please install them first):
1. GSL
2. swig
3. cmpfit 
(https://www.physics.wisc.edu/~craigm/idl/cmpfit.html)
4. pybwidget 
(https://sourceforge.net/projects/topographica/files/external-full-history/pybwidget-0.1.2_1.7.0.tar.gz/download)

### Install:
1. run "python setup.py build_ext --inplace"
2. Add the path to your $PYTHONPATH
3. Add "DASpec_TEMPLATE_PATH" in .bashrc as the directory of template files, e.g., export $DASpec_TEMPLATE_PATH="..."

### Usage:
1. run "DASpec_GUI.py" or "DASpec_GUI_4k.py" (for 4k screen) directly
2. "DASpec_GUI.py -s spectrum_file.txt" (spectrum_file.txt with three columns: wavelength, flux, err)
3. "DASpec_GUI.py -b list.txt" (list.txt is a list of many spectrum files)

### Interface:

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/Interface.png" width="720" height="438">

### Tutorial:

1. Set fitting windows: select the checkboxes and click "Update"

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/fit_wins.png" width="309" height="325">

2. Set components: add or delete the components, and then select the checkboxes

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/Components.png" width="684" height="583">

Here, I used a powerlaw to model the AGN continuum, an Fe II template, a double-Gaussians for the broad component of Hbeta emission line, a Gaussian for each of the narrow emission lines (Hbeta, [OIII]4959,5007). 

3. If you want to tie the profiles of the emission lines: for example, tie component 7 to have the same profile as component 5, and tie the profile of component 6 to 5 with flux ratio 0.3333, then select the checkboxes and click "Update"

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/fit_tie.png" width="571" height="325">

The narrow Hbeta and [OIII]4959 are contrainted to have the same profile as [OIII]5007. And the flux ratio of [OIII]5007/4959 is fixed to 3.

4. Begin fitting: Click lmfit (levenberg-Marquardt method) or mix_fit (similar to Basinhopping in Scipy)

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/fit_buttons.png" width="309" height="145">

5. Check the fitting result

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/Spectrum_window.png" width="564" height="513">

6. You will have an .out file in your working directory

7. If you want to begin from the last fitting: DASpec_GUI.py -s spectrum_file.txt -m spectrum_file.txt.out

### Acknowledgement:
I will appreciate if you can cite DASpec in your paper: e.g., \software{\cb DASpec \url{https://github.com/PuDu-Astro/DASpec}}
