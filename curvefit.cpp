#include "curvefit.h"

curvefit::curvefit()
{
    data_model.n = 0;
    data_model.model = NULL;
    par0 = NULL;
    pout = NULL;
    perrout = NULL;
    nplimit = 0;
    iternum = 0;
    chisq = -99;
    reduced_chisq = -99;
    DOF = -99;
    status = -99;
}

//curvefit::~curvefit()
//{
//    delete plimit;
//    delete pout;
//    delete perrout;
//    delete pout_tot;
//    delete perrout_tot;
//    data_model.n = 0;
//    data_model.model = NULL;
//    par0 = NULL;
//    pout = NULL;
//    perrout = NULL;
//    pout_tot = NULL;
//    perrout_tot = NULL;
//    plimit = NULL;
//    nplimit = 0;
//    iternum = 0;
//    chisq = -99;
//    reduced_chisq = -99;
//    DOF = -99;
//    npout = 0;
//    npout_tot = 0;
//}

void curvefit::setdata(int num, double *x, double *y, double *err)
{
    data_model.n = num;
    data_model.x = x;
    data_model.y = y;
    data_model.err = err;
}

void curvefit::setmodel(compcontainer *m)
{
    data_model.model = m;
    int n = (data_model.model)->netnpar();
    int n_tot = (data_model.model)->npar;
    plimit = new struct struct_parlimit[2 * n];
    nplimit = 0;
    pout = new double[n];
    perrout = new double[n];
    pout_tot = new double[n_tot];
    perrout_tot = new double[n_tot];
    npout = (data_model.model)->netnpar();
    npout_tot = n_tot;
}

void curvefit::setinitp(double *p)
{
    par0 = p;
}

void curvefit::setlimit(int n, double p, int limit)
{
    plimit[nplimit].p = n - 1;
    plimit[nplimit].val = p;
    plimit[nplimit].limit = limit;
    nplimit += 1;
}

//void fitfunc_mpfit(double *p, double *y, int np, int ny, void *data_model)
int fitfunc_mpfit(int ny, int np, double *p, double *deviates, double **derivs
    , struct struct_data_model *data_model)
{
    int n = data_model->n; // ny == n
    if (ny != n)
    {
        std::cout << "Error! ny != n!" << std::endl;
        std::exit(-1);
    }
    double *x = data_model->x;
    double *y = data_model->y;
    double *err = data_model->err;
    compcontainer *model = data_model->model;

    double tempy[n];
    for (int i = 0; i < n; ++i) tempy[i] = 0.0;
    
    model->calc(n, x, tempy, p);
    
    for (int i = 0; i < n; ++i)
    {
        deviates[i] = (tempy[i] - y[i]) / err[i];
    }

    return 0;
}

double fitfunc_siman(int np, double *p, struct struct_data_model *data_model)
{
    int n = data_model->n;
    double *x = data_model->x;
    double *y = data_model->y;
    double *err = data_model->err;
    compcontainer *model = data_model->model;
    double tempy[n];
    for (int i = 0; i < n; ++i) tempy[i] = 0.0;
    model->calc(n, x, tempy, p);
    double chisq = 0.0;
    for (int i = 0; i < n; ++i) chisq += std::pow((tempy[i] - y[i]) / err[i], 2.0);
    return chisq;
}


void curvefit::lmfit(int nitermax)
{
    int npar = (data_model.model)->netnpar();
    double par[npar];
    for (int i = 0; i < npar; ++i) par[i] = par0[i];
    
    mp_result fitresult;
    memset(&fitresult, 0, sizeof(fitresult));
    mp_par parset[npar];
    memset(&parset[0], 0, sizeof(parset));
    double parerr[npar];
    fitresult.xerror = parerr;
    mp_config config;
    memset(&config, 0, sizeof(config));
    config.maxiter = nitermax;
    
    if (nplimit > 0)
    {
        for (int i = 0; i < nplimit; ++i)
        {
            if (plimit[i].limit == 0)
            {
                parset[plimit[i].p].limited[0] = 1;
                parset[plimit[i].p].limits[0] = plimit[i].val;
            }
            else if (plimit[i].limit == 1)
            {
                parset[plimit[i].p].limited[1] = 1;
                parset[plimit[i].p].limits[1] = plimit[i].val;
            }
        }
    }
    
    status = mpfit((mp_func) fitfunc_mpfit, data_model.n, npar, 
        par, parset, &config, &data_model, &fitresult);
        
    for (int i = 0; i < npar; ++i)
    {
        pout[i] = par[i];
        perrout[i] = parerr[i];
    }
    
    iternum = fitresult.niter;
    chisq = fitresult.bestnorm;
    reduced_chisq = fitresult.bestnorm / ((float) (fitresult.nfunc - fitresult.nfree));
    DOF = fitresult.nfunc - fitresult.nfree;
    
    (data_model.model)->pars2l(pout, pout_tot);
    (data_model.model)->parerrs2l(perrout, perrout_tot);
       
    //for (int i = 0; i < npar; ++i) std::cout << par0[i] << " ";
    //std::cout << std::endl; 
    //for (int i = 0; i < npar; ++i) std::cout << par[i] << " ";
    //std::cout << std::endl;
    //for (int i = 0; i < npar; ++i) std::cout << parerr[i] << " ";
    //std::cout << std::endl;
}


void curvefit::siman(int ntmax, int ninner, double jump, int ninit, double Tratio, double delta, 
    int nstable)
{
    int npar = (data_model.model)->netnpar();
    //double par[npar];
    //for (int i = 0; i < npar; ++i) par[i] = par0[i];
    
    /* check if each parameter have been set limits */
    int label[npar];
    double lim1[npar], lim2[npar];
    for (int i = 0; i < npar; ++i) label[i] = 0;
    if (nplimit > 0)
    {
        for (int i = 0; i < nplimit; ++i)
        {
            if (plimit[i].limit == 0)
            {
                lim1[plimit[i].p] = plimit[i].val;
                label[plimit[i].p] += 1;
            }
            else if (plimit[i].limit == 1)
            {
                lim2[plimit[i].p] = plimit[i].val;
                label[plimit[i].p] += 1;
            }
        }
    }
    else
    {
        std::cout << "Error! no limits set! fitting does not run!" << std::endl;
        return;
    }
    for (int i = 0; i < npar; ++i)
    {
        if (label[i] != 2)
        {
            std::cout << "Error! please set limits to all par! fitting does not run!" << std::endl;
            return;
        }
    }
    
    /* === begin simulated annearling fitting === */
    
    /* initialize random number generator */
    
    const gsl_rng_type *T;
    gsl_rng *Random, *Randomc, *Randomi;
    gsl_rng_env_setup();
    T = gsl_rng_default;
    Random = gsl_rng_alloc(T);
    Randomc = gsl_rng_alloc(T);
    Randomi = gsl_rng_alloc(T);
    gsl_rng_set(Random, (unsigned long) time(NULL));
    gsl_rng_set(Randomc, (unsigned long) time(NULL) - 2);
    gsl_rng_set(Randomi, (unsigned long) time(NULL) - 4);
    
    /* determine initial temperature */
    std::cout << "initialize..." << std::endl;
    int n = npar;
    double pinit[n], Einit[ninit], Einitmin, Einitmax;
    for (int iinit = 0; iinit < ninit; ++iinit)
    {
        for (int k = 0; k < n; ++k)
        {
            pinit[k] = lim1[k] + (lim2[k] - lim1[k]) * gsl_rng_uniform_pos(Randomi);
        }
        Einit[iinit] = fitfunc_siman(n, pinit, &data_model);
    }
    Einitmin = Einit[0];
    Einitmax = Einit[0];
    for (int iinit = 0; iinit < ninit; ++iinit)
    {
        if (Einitmin > Einit[iinit])
        {
            Einitmin = Einit[iinit];
        }
        if (Einitmax < Einit[iinit])
        {
            Einitmax = Einit[iinit];
        }
    }
    double Temperature = Einitmax - Einitmin;
    std::cout << "init temperature:" << Temperature << std::endl;
    
    /* begin iteration */
    
    double pbest[n], plast[n], pnew[n];
    double Ebest = 0.0, Enew = 0.0, ratio = jump;
    double prob = 0.0;
    double temp;
    int niter = 0;
    
    for (int i = 0; i < n; ++i) pbest[i] = par0[i];
    Ebest = fitfunc_siman(n, pbest, &data_model);
    
    int nt = ntmax, nj = ninner, stable = 1, n_stable = 0;
    
    for (int i = 0; i < nt; ++i)
    {
        niter += 1;
        for (int k = 0; k < n; ++k) plast[k] = pbest[k];
        for (int j = 0; j < nj; ++j)
        {
            for (int k = 0; k < n; ++k)
            {
                do
                {
                    temp = pbest[k] + ratio * (lim2[k] - lim1[k]) * gsl_ran_gaussian_ziggurat(Random, 1.0);
                } while ((temp < lim1[k]) || (temp > lim2[k]));
                pnew[k] = temp;
            }
            Enew = fitfunc_siman(n, pnew, &data_model);
            if (Enew - Ebest <= 0)
            {
                for (int k = 0; k < n; ++k) pbest[k] = pnew[k];
                Ebest = Enew;
            }
            else
            {
                prob = std::exp(-(Enew - Ebest) / Temperature);
                //std::cout << "--- " << prob << std::endl;
                if (gsl_rng_uniform(Randomc) < prob)
                {
                    for (int k = 0; k < n; ++k) pbest[k] = pnew[k];
                    Ebest = Enew;
                }
            }
        }
        
        stable = 1;
        for (int k = 0; k < n; ++k)
        {
            if (std::fabs((pbest[k] - plast[k]) / plast[k]) > delta)
            {
                stable = 0;
                n_stable = 0;
            }
        }
        if (stable == 1)
        {
            n_stable += 1;
        }
        if (n_stable >= nstable)
        {
            break;
        }
        
        Temperature /= 1.0 + Tratio * (1.0 + i); 
        //Temperature /= 1.0 + std::log10(1.0 + Tratio * (1.0 + i));
        std::cout << "temperature: " << Temperature << " chisq: " << Ebest << " par: "; //<< std::endl;
        for (int k = 0; k < n; ++k) std::cout << pbest[k] << " ";
        std::cout << std::endl;
    }
    
    for (int i = 0; i < npar; ++i)
    {
        pout[i] = pbest[i];
        perrout[i] = -99.0;
    }
    
    iternum = niter;
    chisq = Ebest;
    DOF = data_model.n - npar + 1;
    reduced_chisq = Ebest / ((float) DOF);
    
    (data_model.model)->pars2l(pout, pout_tot);
    (data_model.model)->parerrs2l(perrout, perrout_tot);
    
    gsl_rng_free(Random);
    gsl_rng_free(Randomc);
    gsl_rng_free(Randomi);
}

void curvefit::mix_fit(int ntmax, int ninner, double jump, int ninit, double Tratio, double delta, 
        int nstable)
{
    int npar = (data_model.model)->netnpar();
    
    /* check if each parameter have been set limits */
    int label[npar];
    double lim1[npar], lim2[npar];
    for (int i = 0; i < npar; ++i) label[i] = 0;
    if (nplimit > 0)
    {
        for (int i = 0; i < nplimit; ++i)
        {
            if (plimit[i].limit == 0)
            {
                lim1[plimit[i].p] = plimit[i].val;
                label[plimit[i].p] += 1;
            }
            else if (plimit[i].limit == 1)
            {
                lim2[plimit[i].p] = plimit[i].val;
                label[plimit[i].p] += 1;
            }
        }
    }
    else
    {
        std::cout << "Error! no limits set! fitting does not run!" << std::endl;
        return;
    }
    for (int i = 0; i < npar; ++i)
    {
        if (label[i] != 2)
        {
            std::cout << "Error! please set limits to all par! fitting does not run!" << std::endl;
            return;
        }
    }
    
    /* === begin simulated annearling fitting === */
    
    /* initialize random number generator */
    
    const gsl_rng_type *T;
    gsl_rng *Random, *Randomc, *Randomi;
    gsl_rng_env_setup();
    T = gsl_rng_default;
    Random = gsl_rng_alloc(T);
    Randomc = gsl_rng_alloc(T);
    Randomi = gsl_rng_alloc(T);
    gsl_rng_set(Random, (unsigned long) time(NULL));
    gsl_rng_set(Randomc, (unsigned long) time(NULL) - 2);
    gsl_rng_set(Randomi, (unsigned long) time(NULL) - 4);
    
    /* determine initial temperature */
    std::cout << "initialize..." << std::endl;
    int n = npar;
    double pinit[n], Einit[ninit], Einitmin, Einitmax;
    for (int iinit = 0; iinit < ninit; ++iinit)
    {
        for (int k = 0; k < n; ++k)
        {
            pinit[k] = lim1[k] + (lim2[k] - lim1[k]) * gsl_rng_uniform_pos(Randomi);
        }
        Einit[iinit] = fitfunc_siman(n, pinit, &data_model);
    }
    Einitmin = Einit[0];
    Einitmax = Einit[0];
    for (int iinit = 0; iinit < ninit; ++iinit)
    {
        if (Einitmin > Einit[iinit])
        {
            Einitmin = Einit[iinit];
        }
        if (Einitmax < Einit[iinit])
        {
            Einitmax = Einit[iinit];
        }
    }
    double Temperature = Einitmax - Einitmin;
    std::cout << "init temperature:" << Temperature << std::endl;
    
    /* initialize lmfit */
    double par[npar];
    double parerr[npar];
    mp_result fitresult;
    mp_par parset[npar];
    memset(&parset[0], 0, sizeof(parset));
    if (nplimit > 0)
    {
        for (int i = 0; i < nplimit; ++i)
        {
            if (plimit[i].limit == 0)
            {
                parset[plimit[i].p].limited[0] = 1;
                parset[plimit[i].p].limits[0] = plimit[i].val;
            }
            else if (plimit[i].limit == 1)
            {
                parset[plimit[i].p].limited[1] = 1;
                parset[plimit[i].p].limits[1] = plimit[i].val;
            }
        }
    }
    
    /* begin iteration */
    
    double pbest[n], plast[n], pnew[n];
    double Ebest = 0.0, Enew = 0.0, ratio = jump;
    double Ebest_global = 0.0, pbest_global[n], perrbest_global[n];
    double Elmfit = 0.0;
    double prob = 0.0;
    double temp;
    int niter = 0;
    
    for (int i = 0; i < n; ++i) pbest[i] = par0[i];
    Ebest = fitfunc_siman(n, pbest, &data_model);

    for (int i = 0; i < n; ++i) pbest_global[i] = pbest[i];
    Ebest_global = Ebest;
    
    int nt = ntmax, nj = ninner, stable = 1, n_stable = 0;
    
    for (int i = 0; i < nt; ++i)
    {
        niter += 1;
        for (int k = 0; k < n; ++k) plast[k] = pbest[k];
        for (int j = 0; j < nj; ++j)
        {
            for (int k = 0; k < n; ++k)
            {
                do
                {
                    temp = pbest[k] + ratio * (lim2[k] - lim1[k]) * gsl_ran_gaussian_ziggurat(Random, 1.0);
                } while ((temp < lim1[k]) || (temp > lim2[k]));
                pnew[k] = temp;
            }
            Enew = fitfunc_siman(n, pnew, &data_model);
            if (Enew - Ebest <= 0)
            {
                for (int k = 0; k < n; ++k) pbest[k] = pnew[k];
                Ebest = Enew;
            }
            else
            {
                prob = std::exp(-(Enew - Ebest) / Temperature);
                //std::cout << "--- " << prob << std::endl;
                if (gsl_rng_uniform(Randomc) < prob)
                {
                    for (int k = 0; k < n; ++k) pbest[k] = pnew[k];
                    Ebest = Enew;
                }
            }
        }
        
        /* lmfit */
        for (int k = 0; k < npar; ++k) par[k] = pbest[k];
        
        memset(&fitresult, 0, sizeof(fitresult));
        fitresult.xerror = parerr;
        
        status = mpfit((mp_func) fitfunc_mpfit, data_model.n, npar, 
          par, parset, 0, &data_model, &fitresult);

        Elmfit = fitfunc_siman(n, par, &data_model);
        if (Elmfit < Ebest)
        {
            for (int k = 0; k < npar; ++k)
            {
                pbest[k] = par[k];
                //perrout[k] = parerr[k];
            }
            Ebest = fitfunc_siman(n, pbest, &data_model);
        }

        if (Ebest_global > Ebest)
        {
            for (int k = 0; k < n; ++k) pbest_global[k] = par[k];
            for (int k = 0; k < n; ++k) perrbest_global[k] = parerr[k];
            Ebest_global = Ebest;
        }
        
        stable = 1;
        for (int k = 0; k < n; ++k)
        {
            if (std::fabs((pbest[k] - plast[k]) / plast[k]) > delta)
            {
                stable = 0;
                n_stable = 0;
            }
        }
        if (stable == 1)
        {
            n_stable += 1;
        }
        if (n_stable >= nstable)
        {
            break;
        }
        
        Temperature /= 1.0 + Tratio * (1.0 + i); 
        //Temperature /= 1.0 + std::log10(1.0 + Tratio * (1.0 + i));
        std::cout << "temperature: " << Temperature << " chisq: " << Ebest << " par: "; //<< std::endl;
        for (int k = 0; k < n; ++k) std::cout << pbest[k] << " ";
        std::cout << std::endl;
    }

    if (Ebest_global < Ebest)
    {
        for (int k = 0; k < n; ++k) 
        {
            pout[k] = pbest_global[k];
            perrout[k] = perrbest_global[k];
        }
        Ebest = Ebest_global;
    }
    else
    {
        for (int i = 0; i < npar; ++i)
        {
            pout[i] = pbest[i];
            perrout[i] = parerr[i];
        }
    }
    
    iternum = niter;
    chisq = Ebest;
    DOF = data_model.n - npar + 1;
    reduced_chisq = Ebest / ((float) DOF);
    
    (data_model.model)->pars2l(pout, pout_tot);
    (data_model.model)->parerrs2l(perrout, perrout_tot);
    
    gsl_rng_free(Random);
    gsl_rng_free(Randomc);
    gsl_rng_free(Randomi);
    
}        

void curvefit::info()
{
    std::cout << "status: " << status << " ";
    std::cout << "iternum: " << iternum << " ";
    std::cout << "chisq: " << chisq << " ";
    std::cout << "reduced-chisq: " << reduced_chisq << " ";
    std::cout << "DOF: " << DOF << " " << std::endl;
}
