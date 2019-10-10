#ifndef _CURVEFIT_H_
#define _CURVEFIT_H_

#include "mpfit.h"
#include "common.h"
#include "compcontainer.h"
#include <string.h>
#include <time.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_sort.h>
#include <gsl/gsl_statistics.h>


struct struct_data_model
{
    int n;
    double *x;
    double *y;
    double *err;
    compcontainer *model;
};

//struct struct_data_model_par
//{
//    struct struct_data_model *data_model;
//    double *par;
//    struct struct_parlimit *parlimit;
//    int nparlimit;
//};

struct struct_parlimit
{
    int p; // number in par array;
    double val; // limit value
    double limit; // 0: lower limit, 1: upper limit
};

int fitfunc_mpfit(int ny, int np, double *p, double *deviates, double **derivs
    , struct struct_data_model *data_model);
    
double fitfunc_siman(int np, double *p, struct struct_data_model *data_model);  

class curvefit
{
public:
    curvefit();
    //~curvefit();
    
    struct struct_data_model data_model;
    double *par0; // initial guess of parameters
    double *pout, *perrout; // output parameters and errors
    double *pout_tot, *perrout_tot; // output parameters and errors
    int nplimit, npout, npout_tot;
    struct struct_parlimit *plimit;
    int iternum;
    double chisq, reduced_chisq;
    double DOF;
    int status;
    
    void setdata(int num, double *x, double *y, double *err);
    void setmodel(compcontainer *m);
    void setinitp(double *p);
    void setlimit(int n, double p, int limit);
    
    void lmfit(int nitermax = 200);
    void siman(int ntmax = 1000, int ninner = 500, double jump = 0.03, 
        int ninit = 1000, double Tratio = 0.02, double delta = 1.0e-6, int nstable = 25);
    void mix_fit(int ntmax, int ninner, double jump, int ninit, double Tratio, double delta, 
        int nstable);
    
    void info();
};

#endif
