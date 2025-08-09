# DASpec
## Decomposition of AGN Spectrum (DASpec)
A multi-component spectral fitting code for active galactic nuclei with GUI interface

(*Advantage of this code: You can tie the width or shift of an emission line to those of another one, or fix any parameter to a specific value as you like*)

based on Python 3

Version: 0.9

Author: Pu Du

email: dupu@ihep.ac.cn

### Dependency (please install them first):
1. GSL
2. swig
3. cmpfit 
(https://www.physics.wisc.edu/~craigm/idl/cmpfit.html)
4. Bwidget & pybwidget 
(apt install bwidget & https://sourceforge.net/projects/topographica/files/external-full-history/pybwidget-0.1.2_1.7.0.tar.gz/download for pybwidget)

### Install:
1. edit paths in setup.py to include GSL and cmpfit headers and libraries
2. run "python setup.py build_ext --inplace"
3. Add the path to your $PYTHONPATH
4. Add "DASpec_TEMPLATE_PATH" in .bashrc as the directory of template files, e.g., export DASpec_TEMPLATE_PATH="..."

### Usage:
1. run "DASpec_GUI.py" directly
2. "DASpec_GUI.py -s spectrum_file.txt" (spectrum_file.txt with three columns: wavelength, flux, err)
3. "DASpec_GUI.py -b list.txt" (list.txt is a list of many spectrum files)

### Interface:

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/Interface.png" width="720" height="438">

### Windows sizes:
can be adjuested by "win_geometry" parameter in "DASpec_GUI.py"

### Tutorial:

1. Set fitting windows: select the checkboxes and click "Update"

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/fit_wins.png" width="309" height="325">

2. Set components: add or delete the components, and then select the checkboxes (each component has three lines: input parameters, lower limits and upper limits)

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/Components.png" width="684" height="583">

Each component has 3 lines with several "keywords" appearing only in the first line and the other "to-fit" parameters appearing in all of the three lines.

The "keywords" are some parameters that control the formula of the corresponding component: e.g., lambda_0 in the power law component $F_{lambda} = F_{lambda_0} * (lambda / lambda_0)^alpha$. lambda_0 is a "keyword", and F_{lambda_0} and alpha are the "to-fit" parameters.

Here, I used 

(a) a power law to model the AGN continuum with the parameters of flux and power law index (keyword "5100.0" means the first parameter is the flux at 5100A)

(b) an Fe II template convolved by a Gaussian to model the Fe II emission, with the parameters of flux, width (km/s), and shift (km/s) (keyword "fetemplate_" is the name of the template file which has two columns: wavelength and flux, keywords "4434.0" and "4684.0" mean that the first "to-fit" parameter is the integrated flux from 4434.0 and 4684.0)

(c) a double-Gaussians for the broad component of Hbeta emission line with the parameters of flux, width of the first Gaussian, shift of the first Gaussian, width of the second Gaussian, shift of the second Gaussian, and the ratio of the first to the total line flux (keyword "4861.0" means the line center is located at 4861.0A, the shift and width are calculated relavtive to this center wavelength)

(d) a Gaussian for each of the narrow emission lines with the parameters of flux, width, and shift (Hbeta, [OIII]4959,5007). 

3. If you want to tie the profiles of the emission lines: for example, tie component 7 to have the same profile as component 5, and tie the profile of component 6 to 5 with flux ratio 0.3333, then select the checkboxes and click "Update"

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/fit_tie.png" width="571" height="325">

The narrow Hbeta and [OIII]4959 are contrainted to have the same profile as [OIII]5007. And the flux ratio of [OIII]5007/4959 is fixed to be 3.

4. Begin fitting: Click lmfit (levenberg-Marquardt method) or mix_fit (similar to Basinhopping in Scipy)

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/fit_buttons.png" width="309" height="145">

5. Check the fitting result

<img src="https://github.com/PuDu-Astro/images_for_doc/blob/master/Spectrum_window.png" width="564" height="513">

6. You will have an .out file in your working directory

7. If you want to begin from the last fitting: DASpec_GUI.py -s spectrum_file.txt -m spectrum_file.txt.out

8. You can also fix the value of a parameter to a specific value in "Fix" window.

9. You can use "DASpec_extract_result.py" to read the output file. It is a python class and can separate the names, windows, pars, etc., from the output file. But you need to write your own code to import this python class. Please see "plot.py" as an example how to use "DASpec_extract_result.py".

10. If you perform fitting multiple times for a single object, you will find that there is a long output file. "DASpec_reduce.py" can do some cleaning to the output file and only keep the last fitting for each object: "DASpec_reduce.py *.out".

11. If you would like to subtract any components (e.g., components 3, 4, and 5) from the spectra: DASpec_subtract_components.py spectrum_file.txt.out 3 4 5.

### Acknowledgement:
I will appreciate if you can cite DASpec in your paper: e.g., \software{\citep{Du2024}} and \bibitem[Du(2024)]{Du2024} Du, P.\ 2024, DASpec: A code for spectral decomposition of active galactic nuclei, v0.8, Zenodo, doi:10.5281/zenodo.12578528
