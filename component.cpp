#include "common.h"
#include "function.h"
#include "component.h"

/* ========== member function of class line_gaussian ========== */

// constructor
line_gaussian::line_gaussian(double c)
{
	npar = 3;
	center = c;
	name = "line_gaussian";
	profile = "gaussian";
    for (int i = 0; i < npar; ++i) par[i] = 0.0;
}

// print information
void line_gaussian::info()
{
	std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout << "center:" << " " << center << " ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
	std::cout << "flux:" << " " << par[0] << " ";
	std::cout << "fwhm:" << " " << par[1] << " ";
    std::cout << "shift:" << " " << par[2] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

/* 
calculate profile

num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)
p[0]: flux (erg/s/cm2)
p[1]: FWHM (km/s)
p[2]: shift (km/s)
*/
void line_gaussian::calc(int num, double *x, double *y, double *p)
{
	for (int i = 0; i < npar; ++i) par[i] = p[i];

    double plinear[npar];
	plinear[0] = p[0];
	plinear[2] = p[2] / 3.0e5 * center + center;
    plinear[1] = p[1] / 3.0e5 * plinear[2];
    
    gaussian(num, x, y, plinear);
}

/* ========== member function of class line_dgaussian ========== */

// constructor
line_dgaussian::line_dgaussian(double c)
{
	npar = 6;
	center = c;
	name = "line_dgaussian";
	profile = "dgaussian";
    for (int i = 0; i < npar; ++i) par[i] = 0.0;
}

// print information
void line_dgaussian::info()
{
	std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout << "center:" << " " << center << " ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
	std::cout << "flux:" << " " << par[0] << " ";
	std::cout << "fwhm1:" << " " << par[1] << " ";
    std::cout << "shift1:" << " " << par[2] << " ";
    std::cout << "fwhm2:" << " " << par[3] << " ";
    std::cout << "shift2:" << " " << par[4] << " ";
    std::cout << "fraction1:" << " " << par[5] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

/*
 calc: calculate the component
 p[0]: flux (erg/s/cm2)
 p[1]: FWHM (km/s)
 p[2]: shift (km/s)
 p[3]: FWHM (km/s)
 p[4]: shift (km/s)
 p[5]: flux ratio (1/(1+2))
*/
void line_dgaussian::calc(int num, double *x, double *y, double *p)
{
	for (int i = 0; i < npar; ++i) par[i] = p[i];

    double plinear[npar];
	plinear[0] = p[0];
	plinear[2] = p[2] / 3.0e5 * center + center;
    plinear[1] = p[1] / 3.0e5 * plinear[2];
    plinear[4] = p[4] / 3.0e5 * center + center;
    plinear[3] = p[3] / 3.0e5 * plinear[4];
    plinear[5] = p[5];
    
    dgaussian(num, x, y, plinear);
}

/* ========== member function of class line_lorentzian ========== */

// constructor
line_lorentzian::line_lorentzian(double c)
{
	npar = 3;
	center = c;
	name = "line_lorentzian";
	profile = "lorentzian";
    for (int i = 0; i < npar; ++i) par[i] = 0.0;
}

// print information
void line_lorentzian::info()
{
	std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout << "center:" << " " << center << " ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
	std::cout << "flux:" << " " << par[0] << " ";
	std::cout << "fwhm:" << " " << par[1] << " ";
    std::cout << "shift:" << " " << par[2] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

/* 
calculate profile

num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)
p[0]: flux (erg/s/cm2)
p[1]: FWHM (km/s)
p[2]: shift (km/s)
*/
void line_lorentzian::calc(int num, double *x, double *y, double *p)
{
	for (int i = 0; i < npar; ++i) par[i] = p[i];

    double plinear[npar];
	plinear[0] = p[0];
	plinear[2] = p[2] / 3.0e5 * center + center;
    plinear[1] = p[1] / 3.0e5 * plinear[2];
    
    lorentzian(num, x, y, plinear);
}

/* ========== member function of class powerlaw ========== */
powerlaw::powerlaw(double r)
{
    npar = 2;
	ref = r;
	name = "powerlaw";
	profile = "none";
    for (int i = 0; i < npar; ++i) par[i] = 0.0;
}

void powerlaw::info()
{
	std::cout << "name:" << " " << name << " ";
	std::cout << "ref:" << " " << ref << " ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
	std::cout << "flux:" << " " << par[0] << " ";
    std::cout << "index:" << " " << par[1] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

void powerlaw::calc(int num, double *x, double *y, double *p)
{
	for (int i = 0; i < npar; ++i) par[i] = p[i];
    
    for (int i = 0; i < num; ++i)
    {
        y[i] += p[0] * std::pow(x[i] / ref, p[1]);
    }
}

/* ========== member function of class line_gh4 ========== */

line_gh4::line_gh4(double c)
{
    npar = 5;
	center = c;
	name = "line_gh4";
	profile = "gh4";
    for (int i = 0; i < npar; ++i) par[i] = 0.0;
}

void line_gh4::info()
{
    std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout << "center:" << " " << center << " ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
	std::cout << "flux:" << " " << par[0] << " ";
	std::cout << "sigma:" << " " << par[1] << " ";
    std::cout << "shift:" << " " << par[2] << " ";
    std::cout << "skewness" << " " << par[3] << " ";
    std::cout << "kurtosis:" << " " << par[4] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

void line_gh4::calc(int num, double *x, double *y, double *p)
{
    for (int i = 0; i < npar; ++i) par[i] = p[i];
    
    double plinear[npar];
	plinear[0] = p[0];
	plinear[2] = p[2] / 3.0e5 * center + center;
    plinear[1] = p[1] / 3.0e5 * plinear[2];
    plinear[3] = p[3];
    plinear[4] = p[4];
    
    gh4(num, x, y, plinear);
}

/* ========== member function of class template ========== */

//template_spec::~template_spec()
//{
//    delete [] templatex;
//    delete [] templatey;
//}

template_spec::template_spec(int n, double *x, double *y, std::string k, double f_llim, double f_rlim)
{
    /* 
    create interpolated array with uniform step length 
    
    A. If template already has uniform step and smaller than TEMPLATE_STEP: 
    keep the original template.
    
    B. If template already has uniform step but larger than TEMPLATE_STEP: 
    interpolate to make step == TEMPLATE_STEP.
    
    C. If template has non-uniform step but the largest step smaller than TEMPLATE_STEP: 
    interpolate to make step == the smallest step.
    
    D. If template has non-uniform step but the largest step larer than TEMPLATE_STEP: 
    1. the smallest step <= TEMPLATE_STEP: use the smallest step;
    2. the smallest step > TEMPLATE_STEP: use TEMPLATE_STEP.
    */

    int uniform = checkuniform(n, x, y);
    double dxmin = smalleststep(n, x, y);
    double dxmax = largeststep(n, x, y);
    int rebin;
    double dlnl;
    if (uniform == 1)
    {
        if (dxmin <= TEMPLATE_STEP)
        {
            rebin = 0;
        }
        else if (dxmin > TEMPLATE_STEP)
        {
            rebin = 1;
            dlnl = TEMPLATE_STEP / 3.0e5;
        }
    }
    else if (uniform == 0)
    {
        if (dxmax <= TEMPLATE_STEP)
        {
            rebin = 1;
            dlnl = dxmin;
        }
        else if (dxmax > TEMPLATE_STEP)
        {
            if (dxmin <= TEMPLATE_STEP)
            {
                rebin = 1;
                dlnl = dxmin;
            }
            else if (dxmin > TEMPLATE_STEP)
            {
                rebin = 1;
                dlnl = TEMPLATE_STEP / 3.0e5;
            }
        }
    }
    else
    {
        std::cout << "Error in reading template!" << std::endl;
        std::exit(-1);
    }
    
    if (rebin == 0)
    {
        if (n > NTEMPLATE_MAX)
        {
            std::cout << "Error! please enlarge NTEMPLATE_MAX to ";
            std::cout << n << std::endl;
            std::exit(-1);
        }
        templaten = n;
        templatex = new double[templaten];
        templatey = new double[templaten];
        for (int i = 0; i < templaten; ++i)
        {
            templatex[i] = x[i];
            templatey[i] = y[i];
        }
    }
    else if (rebin == 1)
    {
        double xlim1 = std::log(x[0]), xlim2 = std::log(x[n - 1]);
        int tempnum = (xlim2 - xlim1) / dlnl + 1;
        if (tempnum > NTEMPLATE_MAX)
        {
            std::cout << "Error! please enlarge NTEMPLATE_MAX to ";
            std::cout << tempnum << std::endl;
            std::exit(-1);
        }
        templaten = tempnum;
        templatex = new double[templaten];
        templatey = new double[templaten];
        for (int i = 0; i < templaten; ++i)
        {
            templatex[i] = std::exp(xlim1 + ((double) i) * dlnl);
            templatey[i] = 0.0;
        }
        templatey[0] = y[0];
        templatey[templaten - 1] = y[n - 1];
        int j = 0;
        for (int i = 1; i < templaten - 1; ++i)
        {
            while (1)
            {
                if (templatex[i] >= x[j])
                {
                    j += 1;
                }
                else
                {
                    break;
                }
            }
            templatey[i] = y[j - 1] + (y[j] - y[j - 1]) / (x[j] - x[j - 1]) 
                * (templatex[i] - x[j - 1]);
        }
    }
    
    /* interpolate done */
    
    /* normalize to make flux in the range of flux_llim to flux_rlim to 1 */
    
    flux_llim = f_llim;
    flux_rlim = f_rlim;
    
    double tempflux = 0.0;
    for (int i = 0; i < templaten; ++i)
    {
        if ((templatex[i] >= flux_llim) && (templatex[i] <= flux_rlim))
        {
            tempflux += templatey[i] * (templatex[i] - templatex[i - 1]);
        }
    }
    
    double ratio = 1.0 / tempflux;
    for (int i = 0; i < templaten; ++i) templatey[i] *= ratio;
    
    /* normalize done */
    
    kernel = k;
    
    if (kernel == "gaussian")
    {
        npar = 3;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "gaussian";
    }
    else if (kernel == "lorentzian")
    {
        npar = 3;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "lorentzian";
    }
    else if (kernel == "dgaussian")
    {
        npar = 6;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "dgaussian";
    }
    else if (kernel == "gh4")
    {
        npar = 5;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "gh4";
    }
    else
    {
        std::cout << "Error! no such kernel!" << std::endl;
        std::exit(-1);
    }
}

void template_spec::info()
{
    std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout << "kernel:" << " " << kernel << " ";
    std::cout << "length:" << " " << templaten << " ";
    std::cout << "flux range:" << " (" << flux_llim << "," << flux_rlim << ") ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
    if (kernel == "gaussian")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "fwhm:" << " " << par[1] << " ";
        std::cout << "shift:" << " " << par[2] << std::endl;
    }
    else if (kernel == "lorentzian")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "fwhm:" << " " << par[1] << " ";
        std::cout << "shift:" << " " << par[2] << std::endl;
    }
    else if (kernel == "dgaussian")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "fwhm1:" << " " << par[1] << " ";
        std::cout << "shift1:" << " " << par[2] << " ";
        std::cout << "fwhm2:" << " " << par[3] << " ";
        std::cout << "shift2:" << " " << par[4] << " ";
        std::cout << "fraction1:" << " " << par[5] << std::endl;
    }
    else if (kernel == "gh4")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "sigma:" << " " << par[1] << " ";
        std::cout << "shift:" << " " << par[2] << " ";
        std::cout << "skewness" << " " << par[3] << " ";
        std::cout << "kurtosis:" << " " << par[4] << std::endl;
    }
    std::cout.unsetf(std::ios::scientific);
}

void template_spec::calc(int num, double *x, double *y, double *p)
{
    for (int i = 0; i < npar; ++i) par[i] = p[i];
    
    /* find range of array to be convolved */
    int i;
    double x1, x2;
    x1 = x[0];
    x2 = x[num - 1];
    for (i = 0; i < num; ++i)
    {
        if (x[i] < x1)
        {
            x1 = x[i];
        }
        if (x[i] > x2)
        {
            x2 = x[i];
        }
    }
    x1 = std::log(x1);
    x2 = std::log(x2);
    
    double dfwhm = 0.0, dshift = 0.0;
    if (kernel == "gaussian")
    {
        dfwhm = p[1];
        dshift = p[2];
    }
    else if (kernel == "lorentzian")
    {
        dfwhm = p[1];
        dshift = p[2];
    }
    else if (kernel == "dgaussian")
    {
        dfwhm = std::fabs(p[1]) + std::fabs(p[3]);
        dshift = std::fabs(p[2]) + std::fabs(p[4]);
    }
    else if (kernel == "gh4")
    {
        dfwhm = p[1] * 5.0;
        dshift = p[2];
    }
    else
    {
        std::cout << "Error! no such kernel type!" << std::endl;
        std::exit(-1);
    }
    
    double c = 3.0e5;
    dfwhm = dfwhm / c;
    dshift = std::fabs(dshift) / c;
    
    x1 = x1 - ((double) CONVOLVE_FACTOR) / 2.0 * (dfwhm + dshift);
    x2 = x2 + ((double) CONVOLVE_FACTOR) / 2.0 * (dfwhm + dshift);
    
    x1 = std::exp(x1);
    x2 = std::exp(x2);
    
    int nbegin = 0, ntemp = 0;
    for (i = 0; i < templaten; ++i)
    {
        if (templatex[i] >= x1)
        {
            nbegin = i;
            break;
        }
    }
    for (i = nbegin; i < templaten; ++i)
    {
        if (templatex[i] <= x2)
        {
            ntemp += 1;
        }
    }
    
    /* create convolved template */
    double temp[ntemp];
    for (i = 0; i < ntemp; ++i)
    {
        temp[i] = 0.0;
    }
    convolve(ntemp, &templatex[nbegin], &templatey[nbegin], temp, p, kernel);

    /* flux normalization */
    double sum = 0.0;
    for (i = 0; i < ntemp; ++i)
    {
        if ((templatex[nbegin + i] >= flux_llim) && (templatex[nbegin + i] <= flux_rlim))
        {
            sum += temp[i] * (templatex[nbegin + i] - templatex[nbegin + i - 1]);
        }
    }

    //printf("sum: %e %f %f\n", sum, flux_llim, flux_rlim);
    
    /* interpolate */
    
    int j = 0;
    for (i = 0; i < num; ++i)
    {
        if (x[i] < templatex[nbegin])
        {
            y[i] += 0.0;
        }
        else if (x[i] > templatex[nbegin + ntemp - 1])
        {
            y[i] += 0.0;
        }
        else
        {
            while (1)
            {
                if ((x[i] >= templatex[nbegin + j]) && (x[i] < templatex[nbegin + j + 1]))
                {
                    y[i] += (temp[j] + (temp[j + 1] - temp[j]) 
                        / (templatex[nbegin + j + 1] - templatex[nbegin + j])
                        * (x[i] - templatex[nbegin + j])) * p[0] / sum;
                    break;
                }
                else
                {
                    j += 1;
                }
            }
        }
    }
}

balmer_continuum::balmer_continuum()
{
    npar = 2;
	name = "balmer_continuum";
	profile = "gaussian";
    for (int i = 0; i < npar; ++i) par[i] = 0.0;
}


void balmer_continuum::ngaussian(int num, double *x, double *y, int np, double *p)
{
    /* gauss = a * exp(-(x - b)^2 / (2 * c^2))
     * np: number of gauss
     * p[0]: flux (erg/s/cm2/A), p[0] = a * c * (2 * pi)^0.5
     * p[1]: center (Angstroms), p[1] = b
     * p[2]: fhwm (Angstroms), p[2] = 2 * (2 * ln2)^0.5 * c */
    double a, b, c;
    int i, j;
    double temp = std::pow(2.0 * std::log(2.0), 0.5);
        
    for (j = 0; j < np; j++)
    {
        b = p[1 + 3 * j];
        c = p[2 + 3 * j] / (2.0 * temp);
        a = p[0 + 3 * j] / c / SQRT2PI;
        for (i = 0; i < num; i++)
        {
            y[i] += a * std::exp(-(x[i] - b) * (x[i] - b) / 2.0 / c / c);
        }
    }
}

// print information
void balmer_continuum::info()
{
	std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
	std::cout << "flux at Balmer edge:" << " " << par[0] << " ";
    std::cout << "optical depth of Balmer edge:" << " " << par[1] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

void balmer_continuum::calc(int num, double *x, double *y, double *p)
{
    for (int i = 0; i < npar; ++i) par[i] = p[i];
    
    /* create temp wavlength and flux arrays from 500A to 5000A with step 1000km/s */
    int i;
    double xlim1 = 810.0, xlim2 = 4300.0;  // Angstroms
    double dlnl = 1000.0 / 3.0e5;  // 1000km/s
    xlim1 = std::log(xlim1);
    xlim2 = std::log(xlim2);
    int nbalc = (xlim2 - xlim1) / dlnl + 1;
    double xbalc[nbalc], ybalc[nbalc];
    
    for (i = 0; i < nbalc; ++i)
    {
        xbalc[i] = std::exp(xlim1 + ((double) i) * dlnl);
        ybalc[i] = 0.0;
        //printf("%i %f %f\n", i, xbalc[i], ybalc[i]);
    }
    
    /* calculate balmer continuum */
    double lambda_be = 3646.0; // Angstrom
    double F_be, tau_be, tau_lambda, lambda;
    double B_lambda, Te = 15000.0;
    double h = 6.626e-27, kb = 1.38e-16, c = 2.9979e10;
    double width = 8000.0; // km/s
    
    F_be = 1.0;
    tau_be = p[1];
    
    /* Balc intensity at balmer edge */
    double F_edge = 0.0;
    lambda = lambda_be * 1.0e-8;
    tau_lambda = tau_be * std::pow(lambda_be / lambda_be, 3);
    B_lambda = 2.0 * h * c * c / std::pow(lambda, 5)
        / (std::exp(h * c / lambda / kb / Te) - 1.0);
    F_edge += F_be * B_lambda * (1.0 - std::exp(-tau_lambda));
    
    F_be = F_be / F_edge * p[0]; // change intensity at edge to p[0]
    
    /* wavelength shorter than Balmer edge */
    for (i = 0; i < nbalc; ++i)
    {
        if (xbalc[i] <= lambda_be)
        {
            lambda = xbalc[i] * 1.0e-8;
            tau_lambda = tau_be * std::pow(xbalc[i] / lambda_be, 3);
            B_lambda = 2.0 * h * c * c / std::pow(lambda, 5)
                / (std::exp(h * c / lambda / kb / Te) - 1.0);
            ybalc[i] += F_be * B_lambda * (1.0 - std::exp(-tau_lambda));
            //sum += ybalc[i] * (xbalc[i + 1] - xbalc[i]);
        }
    }
    
    /* Gauss_legendre integration */
    double inte_lim1 = 50.0, inte_lim2 = 3646.0;
    int j;
    double xr, xm, dx, s = 0.0;
    static double xx[] = {0.0, 0.1488743389, 0.4333953941
        , 0.6794095682, 0.8650633666, 0.9739065285};
    static double w[] = {0.0, 0.2955242247, 0.2692667193
        ,0.2190863625,0.1494513491,0.0666713443};
    xm = 0.5 * (inte_lim2 + inte_lim1);
    xr = 0.5 * (inte_lim2 - inte_lim1);
    double func1, func2;
    for (j = 1; j <= 5; ++j)
    {
        dx = xr * xx[j];
        lambda = (xm + dx) * 1.0e-8;
        tau_lambda = tau_be * std::pow(lambda / (lambda_be * 1.0e-8), 3);
        B_lambda = 2.0 * h * c * c / std::pow(lambda, 5)
            / (std::exp(h * c / lambda / kb / Te) - 1.0);
        func1 = F_be * B_lambda * (1.0 - std::exp(-tau_lambda));

        lambda = (xm - dx) * 1.0e-8;
        tau_lambda = tau_be * std::pow(lambda / (lambda_be * 1.0e-8), 3);
        B_lambda = 2.0 * h * c * c / pow(lambda, 5)
            / (std::exp(h * c / lambda / kb / Te) - 1.0);
        func2 = F_be * B_lambda * (1.0 - std::exp(-tau_lambda));

        s += w[j]*(func1 + func2);
    }
    s *= xr;
    
    /* convolve the balmer continuum at wavelength shorter than balmer edge */
    double pcon[3];
    pcon[0] = 1.0;
    pcon[1] = width;
    pcon[2] = 0.0;
    convolve(nbalc, xbalc, ybalc, ybalc, pcon, "gaussian");
    
    /* wavelength longer than Balmer edge */
    double emissivity[] = {
        6.789E-29,  7.214E-29,  7.675E-29,  8.177E-29,  8.723E-29,  9.319E-29,
        9.970E-29,  1.068E-28,  1.147E-28,  1.233E-28,  1.328E-28,  1.433E-28,
        1.549E-28,  1.678E-28,  1.822E-28,  1.983E-28,  2.164E-28,  2.367E-28,
        2.595E-28,  2.854E-28,  3.149E-28,  3.485E-28,  3.869E-28,  4.312E-28,
        4.824E-28,  5.417E-28,  6.109E-28,  6.919E-28,  7.873E-28,  8.999E-28,
        1.033E-27,  1.192E-27,  1.381E-27,  1.607E-27,  1.878E-27,  2.203E-27,
        2.600E-27,  3.100E-27,  3.761E-27,  4.678E-27,  5.998E-27,  7.961E-27,
        1.100E-26,  1.605E-26,  2.522E-26,  4.391E-26,  8.947E-26,  2.398E-25};
        
    double r = 1.097373e7;
    int nbeg = 7;
    int nline = 50 - nbeg + 1;
    double lambda0, p_gauss[3 * nline];
    double scale = s / (3.95 * pow(Te / 1.0e4, 0.4)) / emissivity[50 - 4];
    
    for (i = nbeg; i <= 50; i++)
    {
        lambda0 = 1.0e10 * 1.0 / (r * (1.0 / pow(2.0, 2) - 1.0 / pow((float) i, 2)));
        p_gauss[0 + (i - nbeg) * 3] = emissivity[50 - i] * scale;
        p_gauss[1 + (i - nbeg) * 3] = lambda0;
        p_gauss[2 + (i - nbeg) * 3] = width / 3.0e5 * lambda0;
        //printf("%i\n", i);
        //printf("%i %e %i %f %i %f\n", 0 + (i - nbeg) * 3, p_gauss[0 + (i - nbeg) * 3]
        //        , 1 + (i - nbeg) * 3, p_gauss[1 + (i - nbeg) * 3], 2 + (i - nbeg) * 3
        //        , p_gauss[2 + (i - nbeg) * 3]);
    }
    
    ngaussian(nbalc, xbalc, ybalc, nline, p_gauss);
    
    /* interpolate original array */
    j = 0;
    for (i = 0; i < num; ++i)
    {
        if (x[i] < xbalc[0])
        {
            y[i] += 0.0;
            //printf("%f %f %i %i %f %f\n", x[i], y[i], j, j + 1, xbalc[j], xbalc[j + 1]);
        }
        else if (x[i] > xbalc[nbalc - 1])
        {
            y[i] += 0.0;
            //printf("%f %f %i %i %f %f\n", x[i], y[i], j, j + 1, xbalc[j], xbalc[j + 1]);
        }
        else
        {
            while (1)
            {
                if ((x[i] >= xbalc[j]) && (x[i] < xbalc[j + 1]))
                {
                    y[i] += ybalc[j] + (ybalc[j + 1] - ybalc[j]) 
                        / (xbalc[j + 1] - xbalc[j]) * (x[i] - xbalc[j]);
                    //printf("%f %f %i %i %f %f\n", x[i], y[i], j, j + 1, xbalc[j], xbalc[j + 1]);
                    break;
                }
                else
                {
                    j += 1;
                }
            }
        }
    }
}

ccm_reddening::ccm_reddening(double r)
{
    npar = 1;
	name = "ccm_reddening";
	profile = "none";
    for (int i = 0; i < npar; ++i) par[i] = 0.0;
    r_v = r;
}

void ccm_reddening::info()
{
    std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
    std::cout << "E(B-V):" << " " << par[4] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

void ccm_reddening::calc(int num, double *x, double *y, double *p)
{
    for (int i = 0; i < npar; ++i) par[i] = p[i];
    
    double ratio[num];
    for (int i = 0; i < num; ++i) ratio[i] = 1.0;
    ccm_unred(num, x, ratio, p[0], ratio, r_v);
    for (int i = 0; i < num; ++i) y[i] /= ratio[i];
}

template_spec_reddened::template_spec_reddened(int n, double *x, double *y, std::string k
	    , double f_llim, double f_rlim, double r)
{
    /* 
    create interpolated array with uniform step length 
    
    A. If template already has uniform step and smaller than TEMPLATE_STEP: 
    keep the original template.
    
    B. If template already has uniform step but larger than TEMPLATE_STEP: 
    interpolate to make step == TEMPLATE_STEP.
    
    C. If template has non-uniform step but the largest step smaller than TEMPLATE_STEP: 
    interpolate to make step == the smallest step.
    
    D. If template has non-uniform step but the largest step larer than TEMPLATE_STEP: 
    1. the smallest step <= TEMPLATE_STEP: use the smallest step;
    2. the smallest step > TEMPLATE_STEP: use TEMPLATE_STEP.
    */

    int uniform = checkuniform(n, x, y);
    double dxmin = smalleststep(n, x, y);
    double dxmax = largeststep(n, x, y);
    int rebin;
    double dlnl;
    if (uniform == 1)
    {
        if (dxmin <= TEMPLATE_STEP)
        {
            rebin = 0;
        }
        else if (dxmin > TEMPLATE_STEP)
        {
            rebin = 1;
            dlnl = TEMPLATE_STEP / 3.0e5;
        }
    }
    else if (uniform == 0)
    {
        if (dxmax <= TEMPLATE_STEP)
        {
            rebin = 1;
            dlnl = dxmin;
        }
        else if (dxmax > TEMPLATE_STEP)
        {
            if (dxmin <= TEMPLATE_STEP)
            {
                rebin = 1;
                dlnl = dxmin;
            }
            else if (dxmin > TEMPLATE_STEP)
            {
                rebin = 1;
                dlnl = TEMPLATE_STEP / 3.0e5;
            }
        }
    }
    else
    {
        std::cout << "Error in reading template!" << std::endl;
        std::exit(-1);
    }
    
    if (rebin == 0)
    {
        if (n > NTEMPLATE_MAX)
        {
            std::cout << "Error! please enlarge NTEMPLATE_MAX to ";
            std::cout << n << std::endl;
            std::exit(-1);
        }
        templaten = n;
        templatex = new double[templaten];
        templatey = new double[templaten];
        for (int i = 0; i < templaten; ++i)
        {
            templatex[i] = x[i];
            templatey[i] = y[i];
        }
    }
    else if (rebin == 1)
    {
        double xlim1 = std::log(x[0]), xlim2 = std::log(x[n - 1]);
        int tempnum = (xlim2 - xlim1) / dlnl + 1;
        if (tempnum > NTEMPLATE_MAX)
        {
            std::cout << "Error! please enlarge NTEMPLATE_MAX to ";
            std::cout << tempnum << std::endl;
            std::exit(-1);
        }
        templaten = tempnum;
        templatex = new double[templaten];
        templatey = new double[templaten];
        for (int i = 0; i < templaten; ++i)
        {
            templatex[i] = std::exp(xlim1 + ((double) i) * dlnl);
            templatey[i] = 0.0;
        }
        templatey[0] = y[0];
        templatey[templaten - 1] = y[n - 1];
        int j = 0;
        for (int i = 1; i < templaten - 1; ++i)
        {
            while (1)
            {
                if (templatex[i] >= x[j])
                {
                    j += 1;
                }
                else
                {
                    break;
                }
            }
            templatey[i] = y[j - 1] + (y[j] - y[j - 1]) / (x[j] - x[j - 1]) 
                * (templatex[i] - x[j - 1]);
        }
    }
    
    /* interpolate done */
    
    /* normalize to make flux in the range of flux_llim to flux_rlim to 1 */
    
    flux_llim = f_llim;
    flux_rlim = f_rlim;
    
    double tempflux = 0.0;
    for (int i = 0; i < templaten; ++i)
    {
        if ((templatex[i] >= flux_llim) && (templatex[i] <= flux_rlim))
        {
            tempflux += templatey[i] * (templatex[i] - templatex[i - 1]);
        }
    }
    
    double ratio = 1.0 / tempflux;
    for (int i = 0; i < templaten; ++i) templatey[i] *= ratio;
    
    /* normalize done */
    
    kernel = k;
    
    if (kernel == "gaussian")
    {
        npar = 3;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "gaussian";
    }
    else if (kernel == "lorentzian")
    {
        npar = 3;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "lorentzian";
    }
    else if (kernel == "dgaussian")
    {
        npar = 6;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "dgaussian";
    }
    else if (kernel == "gh4")
    {
        npar = 5;
        for (int i = 0; i < npar; ++i) par[i] = 0.0;
        name = "template_spec";
        profile = "gh4";
    }
    else
    {
        std::cout << "Error! no such kernel!" << std::endl;
        std::exit(-1);
    }
    
    npar += 1;
    name = "template_spec_reddened";
    r_v = r;
}

//template_spec_reddened::~template_spec_reddened()
//{
//    delete [] templatex;
//    delete [] templatey;
//}

void template_spec_reddened::info()
{
    std::cout << "name:" << " " << name << " ";
	std::cout << "profile:" << " " << profile << " ";
	std::cout << "kernel:" << " " << kernel << " ";
    std::cout << "length:" << " " << templaten << " ";
    std::cout << "flux range:" << " (" << flux_llim << "," << flux_rlim << ") ";
	std::cout.setf(std::ios::scientific);
	std::cout.precision(4);
    if (kernel == "gaussian")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "fwhm:" << " " << par[1] << " ";
        std::cout << "shift:" << " " << par[2] << " ";
    }
    else if (kernel == "lorentzian")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "fwhm:" << " " << par[1] << " ";
        std::cout << "shift:" << " " << par[2] << " ";
    }
    else if (kernel == "dgaussian")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "fwhm1:" << " " << par[1] << " ";
        std::cout << "shift1:" << " " << par[2] << " ";
        std::cout << "fwhm2:" << " " << par[3] << " ";
        std::cout << "shift2:" << " " << par[4] << " ";
        std::cout << "fraction1:" << " " << par[5] << " ";
    }
    else if (kernel == "gh4")
    {
        std::cout << "flux:" << " " << par[0] << " ";
        std::cout << "sigma:" << " " << par[1] << " ";
        std::cout << "shift:" << " " << par[2] << " ";
        std::cout << "skewness" << " " << par[3] << " ";
        std::cout << "kurtosis:" << " " << par[4] << " ";
    }
    
    std::cout << "Rv:" << " " << r_v << " ";
    std::cout << "E(B-V):" << " " << par[npar - 1] << std::endl;
    std::cout.unsetf(std::ios::scientific); 
}

void template_spec_reddened::calc(int num, double *x, double *ynew, double *parnew)
{
    //std::cout << "test: " << npar << std::endl;
    //for (int i = 0; i < npar; ++i) std::cout << parnew[i] << " ";
    for (int i = 0; i < npar; ++i) par[i] = parnew[i];
    
    double p[npar - 1];
    for (int i = 0; i < npar - 1; ++i) p[i] = par[i];
    
    double y[num], ratio[num];
    for (int i = 0; i < num; ++i)
    {
        y[i] = 0;
        ratio[i] = 1.0;
    }
    
    /* find range of array to be convolved */
    int i;
    double x1, x2;
    x1 = x[0];
    x2 = x[num - 1];
    for (i = 0; i < num; ++i)
    {
        if (x[i] < x1)
        {
            x1 = x[i];
        }
        if (x[i] > x2)
        {
            x2 = x[i];
        }
    }
    x1 = std::log(x1);
    x2 = std::log(x2);
    
    double dfwhm = 0.0, dshift = 0.0;
    if (kernel == "gaussian")
    {
        dfwhm = p[1];
        dshift = p[2];
    }
    else if (kernel == "lorentzian")
    {
        dfwhm = p[1];
        dshift = p[2];
    }
    else if (kernel == "dgaussian")
    {
        dfwhm = std::fabs(p[1]) + std::fabs(p[3]);
        dshift = std::fabs(p[2]) + std::fabs(p[4]);
    }
    else if (kernel == "gh4")
    {
        dfwhm = p[1] * 5.0;
        dshift = p[2];
    }
    else
    {
        std::cout << "Error! no such kernel type!" << std::endl;
        std::exit(-1);
    }
    
    double c = 3.0e5;
    dfwhm = dfwhm / c;
    dshift = std::fabs(dshift) / c;
    
    x1 = x1 - ((double) CONVOLVE_FACTOR) / 2.0 * (dfwhm + dshift);
    x2 = x2 + ((double) CONVOLVE_FACTOR) / 2.0 * (dfwhm + dshift);
    
    x1 = std::exp(x1);
    x2 = std::exp(x2);
    
    int nbegin = 0, ntemp = 0;
    for (i = 0; i < templaten; ++i)
    {
        if (templatex[i] >= x1)
        {
            nbegin = i;
            break;
        }
    }
    for (i = nbegin; i < templaten; ++i)
    {
        if (templatex[i] <= x2)
        {
            ntemp += 1;
        }
    }
    
    /* create convolved template */
    double temp[ntemp];
    for (i = 0; i < ntemp; ++i)
    {
        temp[i] = 0.0;
    }
    convolve(ntemp, &templatex[nbegin], &templatey[nbegin], temp, p, kernel);

    /* flux normalization */
    double sum = 0.0;
    for (i = 0; i < ntemp; ++i)
    {
        if ((templatex[nbegin + i] >= flux_llim) && (templatex[nbegin + i] <= flux_rlim))
        {
            sum += temp[i] * (templatex[nbegin + i] - templatex[nbegin + i - 1]);
        }
    }
    
    /* interpolate */
    
    int j = 0;
    for (i = 0; i < num; ++i)
    {
        if (x[i] < templatex[nbegin])
        {
            y[i] += 0.0;
        }
        else if (x[i] > templatex[nbegin + ntemp - 1])
        {
            y[i] += 0.0;
        }
        else
        {
            while (1)
            {
                if ((x[i] >= templatex[nbegin + j]) && (x[i] < templatex[nbegin + j + 1]))
                {
                    y[i] += (temp[j] + (temp[j + 1] - temp[j]) 
                        / (templatex[nbegin + j + 1] - templatex[nbegin + j])
                        * (x[i] - templatex[nbegin + j])) * p[0] / sum;
                    break;
                }
                else
                {
                    j += 1;
                }
            }
        }
    }
    
    ccm_unred(num, x, ratio, parnew[npar - 1], ratio, r_v);
    
    for (int i = 0; i < num; ++i) ynew[i] += y[i] / ratio[i];
}
