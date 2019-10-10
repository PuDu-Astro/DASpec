#ifndef _PROTOTYPE_H_
#define _PROTOTYPE_H_

#include "common.h"

/*
 prototype of component
 
 npar: number of parameters
 par: parameter array (if 10 is not enough, please enlarge this number)
 profile: profile of the component
 name: name of the component
 
 info: print information of the component
 
 calc: calculate the profile
 int num: length of x and y
 double *x: wavelength array (Angstrom)
 double *y: flux array (erg/s/cm2/Angstrom)
 double *p: parameter array
*/
class component
{
public:
	int npar;
	double par[NPAR_MAX];
	std::string profile, name;

	virtual void info(){};
	virtual void calc(int num, double *x, double *y, double *p){};
};

#endif
