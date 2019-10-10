#ifndef _COMPCONTAINER_H_
#define _COMPCONTAINER_H_

#include "common.h"
#include "prototype.h"

/*
 component container
 
 int npar: number of parameters (all of the models)
 int nmodel: number of models
 component *model: array containing pointers to model
 
 info: print information of the component
 
 calc: calculate the model including all of the components
 int num: length of x and y
 double *x: wavelength array (Angstrom)
 double *y: flux array (erg/s/cm2/Angstrom)
 double *p: parameter array
 
 addfix: add fix
 c: component
 p: parameter
 val: value
 
 addtie: add tie
 c: component
 p: parameter
 ct: target component
 pt: target parameter
 type: tie type ("ratio":0, "offset":1)
 val: value (ratio or offset)
*/
class compcontainer
{
public:
    compcontainer();
    //~compcontainer();
    
    int ncomp, npar;
    component *comp[NCOMP_MAX];
    int nfix, ntie;
    int fix[NCOMP_MAX * NPAR_MAX][2];
    double fixval[NCOMP_MAX * NPAR_MAX];
    int tie[NCOMP_MAX * NPAR_MAX][5];
    double tieval[NCOMP_MAX * NPAR_MAX];
    
    void add(component *m);
    void info();
    void calc_totpar(int num, double *x, double *y, double *p);
    void calc(int num, double *x, double *y, double *p);
    void pars2l(double *p, double *ptot);
    void parl2s(double *ptot, double *p);
    void parerrs2l(double *p, double *ptot);
    int findpar(int c, int p);
    void clean();
    void addfix(int c, int p, double val);
    void addtie(int c, int p, int ct, int pt, std::string type, double val);
    void addtie_profile(int c, int ct);
    void addtie_flux_profile(int c, int ct, double val);
    int netnpar();  
};

#endif
