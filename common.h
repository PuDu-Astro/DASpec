#ifndef _COMMON_H_
#define _COMMON_H_

#include <iostream>
#include <cmath>
#include <string>
#include <cstdlib>

#include <gsl/gsl_fft_complex.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_complex.h>
#include <gsl/gsl_complex_math.h>


#define REAL(z, i) ((z)[2 * (i)])
#define IMAG(z, i) ((z)[2 * (i) + 1])

#define NPAR_MAX 10           // maximum number of parameters in a component
#define NCOMP_MAX 100         // maximum number of components
#define NITER_MAX_LMFIT 200   // maximum number of iteration in fitting
#define NTEMPLATE_MAX 100000   // maximum length of the template
#define UNIFORM_LIMIT 1.0e-4  // criteria of uniform check in velocity space
#define TEMPLATE_STEP 30.0    // largest step in the template (km/s)
#define CONVOLVE_FACTOR 10    // (int) enlarge factor in step of the convolution kernel

#endif
