#ifndef _FUNCTION_H_
#define _FUNCTION_H_

#define F2S 2.35482    // FWHM / sigma = 2.35482
#define PI 3.1415926   // PI
#define SQRT2PI 2.5066282532517663 // square root of 2*pi

/*
Gaussian function (linear space) 

num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)

p[0]: flux (erg/s/cm2)
p[1]: FWHM (Angstrom)
p[2]: center (Angstrom)
*/
void gaussian(int num, double *x, double *y, double *p);

/*
Lorentzian function (linear space)

num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)

p[0]: flux (erg/s/cm2)
p[1]: FWHM (Angstrom)
p[2]: center (Angstrom)
*/
void lorentzian(int num, double *x, double *y, double *p);

/*
double Gaussian function (linear space) 

num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)

p[0]: total flux (erg/s/cm2)
p[1]: FWHM (Angstrom)
p[2]: center (Angstrom)
p[3]: FWHM (Angstrom)
p[4]: center (Angstrom)
p[5]: flux ratio (1/(1+2))
*/
void dgaussian(int num, double *x, double *y, double *p);

/* 
Gauss-Hermite polynomials    
      
num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)

p[1]: flux (erg/s/cm2)             
p[2]: sigma (Angstrom)                 
p[3]: center (Angstrom)                 
p[4]: skewness                     
p[5]: kurtosis                                              
*/
void gh4(int num, double *x, double *y, double *p);

/* 
check whether the step length is uniform in velocity space
if uniform return 1, otherwise return 0 
*/
int checkuniform(int n, double *x, double *y);

/* return the smallest step length is in velocity space */
double smalleststep(int n, double *x, double *y);

/* return the largest step length is in velocity space */
double largeststep(int n, double *x, double *y);

/*
return number of convolution kernel array 
fwhm: fwhm/sigma (km/s)
shift (km/s)
dlnw: step length
m: number of output array
*/
int convlv_resp_num(double *p, double dlnw, std::string kernel_type);

/*
convolvution kernel

p: parameters of kernel (in linear space)
m: array length of kernel
kernel_type: type of kernel
*/
void convlv_resp(double *p, double dlnw, int m, double *kernel, std::string kernel_type);

/* 
please make sure the input array x and y have uniform steps in velocity space,
but the array themselves are in wavelength space!!!
The subroutine do "not" check whether the step is uniform in v-space!!!
The subroutine are used to convolve the array y in velocity space.
n:length of the array x and y
x and y: input array
p: parameters array of kernel 
*/ 
void convolve(int n, double *x, double *y, double *yout, double *p, std::string kernel_type);

// wave, flux and err will be replaced by redshift-corrected wave, flux and err
// num: array length
// wave: wavelength (Angstrom)
// flux: flux (erg/s/cm2/A)
// err: error (erg/s/cm2/A)
// z: redshift
void correct_redshift(int num, double *wave, double *flux, double *err
        , double *wave1, double *flux1, double *err1, double z);
        
// name: ccm_unred
// purpose: deredden a flux vector using the CCM 1989 parameterization
// converted from IDL ccm_unred procedure
// INPUT:
// wave - wavelength vector (Angstroms)
// flux - calibrated flux vector, same number of elements as WAVE
// ebv  - color excess E(B-V), scalar. If a negative EBV is supplied,
//        then fluxes will be reddened rather than deredenned.
// r_v - scalar specifying the ratio of total selective extinction 
//       R(V) = A(V) / E(B - V).
// OUTPUT:
// funred - unreddened flux vector, same units and number of elements
//          as flux.
void ccm_unred(int num, double *wave, double *flux, double ebv, double *funred
, double r_v);

#endif