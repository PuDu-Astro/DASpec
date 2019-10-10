#ifndef _COMPONENT_H_
#define _COMPONENT_H_

#include "prototype.h"

/*
 Gaussian line profile
 
 center: center of the line
 
 info: print information of the component
 
 calc: calculate the component
 p[0]: flux (erg/s/cm2)
 p[1]: FWHM (km/s)
 p[2]: shift (km/s)
*/
class line_gaussian : public component
{
public:
    line_gaussian(double c);
    
	double center;

	void info();
	void calc(int num, double *x, double *y, double *p);   
};

/*
 double Gaussian line profile
 
 center: center of the line
 
 info: print information of the component
 
 calc: calculate the component
 p[0]: flux (erg/s/cm2)
 p[1]: FWHM (km/s)
 p[2]: shift (km/s)
 p[3]: FWHM (km/s)
 p[4]: shift (km/s)
 p[5]: flux ratio (1/(1+2))
*/
class line_dgaussian : public component
{
public:
    line_dgaussian(double c);
    
	double center;

	void info();
	void calc(int num, double *x, double *y, double *p);   
};

/*
 Gaussian line profile
 
 center: center of the line
 
 info: print information of the component
 
 calc: calculate the component
 p[0]: flux (erg/s/cm2)
 p[1]: FWHM (km/s)
 p[2]: shift (km/s)
*/
class line_lorentzian : public component
{
public:
    line_lorentzian(double c);
    
	double center;

	void info();
	void calc(int num, double *x, double *y, double *p);
};

/*
 power law
 a * (x / c)^b
 
 ref: c
 
 info: print information of the component
 
 calc: calculate the component
*/
class powerlaw : public component
{
public:
    powerlaw(double r);
    
	double ref;

	void info();
	void calc(int num, double *x, double *y, double *p);
};

/*
 Gauss-Hermite polynomials line profile
 
 center: center of the line
 
 info: print information of the component
 
 calc: calculate the component
 p[0]: flux (erg/s/cm2)
 p[1]: sigma (km/s)
 p[2]: shift (km/s)
 p[3]: skewness
 p[4]: kurtosis
*/
class line_gh4 : public component
{
public:
    line_gh4(double c);
    
	double center;

	void info();
	void calc(int num, double *x, double *y, double *p);   
};

/*
template convolved by a certain kernel
*/
class template_spec : public component
{
public:
    template_spec(int num, double *x, double *y, std::string k, double f_llim = 4434.0, double f_rlim = 4684.0);
    //~template_spec();
    
    int templaten;
    double *templatex, *templatey;
    std::string kernel;
    double flux_llim, flux_rlim;
    
    void info();
    void calc(int num, double *x, double *y, double *p);
};

/*
reddened template convolved by a certain kernel
*/
class template_spec_reddened : public component
{
public:
    template_spec_reddened(int num, double *x, double *y, std::string k
	    , double f_llim = 4434.0, double f_rlim = 4684.0, double r = 3.1);
    //~template_spec_reddened();
    
    int templaten;
    double *templatex, *templatey;
    std::string kernel;
    double flux_llim, flux_rlim;
	double r_v;
    
    void info();
    void calc(int num, double *x, double *y, double *p);
};

/*
balmer continuum
*/
class balmer_continuum : public component
{
public:
    balmer_continuum();
    
    void info();
    void calc(int num, double *x, double *y, double *p);
	
	void ngaussian(int num, double *x, double *y, int np, double *p);
};

/*
ccm reddening
*/
class ccm_reddening : public component
{
public:
    ccm_reddening(double r = 3.1);
	
	double r_v;
    
    void info();
    void calc(int num, double *x, double *y, double *p);
};


#endif