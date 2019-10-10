#include "common.h"
#include "function.h"

/*
gaussian function (linear space) 

num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)
p[0]: flux (erg/s/cm2)
p[1]: FWHM (Angstrom)
p[2]: center (Angstrom)
*/
void gaussian(int num, double *x, double *y, double *p)
{
    double sigma = p[1] / F2S;
    for (int i = 0; i < num; ++i)
    {
        y[i] += p[0] / SQRT2PI / sigma 
            * std::exp(-0.5 * (x[i] - p[2]) * (x[i] - p[2]) / sigma / sigma);
    }
}

/*
Lorentzian function (linear space)

num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)
p[0]: flux (erg/s/cm2)
p[1]: FWHM (Angstrom)
p[2]: center (Angstrom)
*/
void lorentzian(int num, double *x, double *y, double *p)
{
    for (int i = 0; i < num; ++i)
    {
        y[i] += p[0] / PI * 0.5 * p[1] 
            / ((x[i] - p[2]) * (x[i] - p[2]) + 0.5 * p[1] * 0.5 * p[1]);
    }
}

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
void dgaussian(int num, double *x, double *y, double *p)
{
    double flux1 = p[0] * p[5];
    double flux2 = p[0] * (1.0 - p[5]);
    double p1[3];
    double p2[3];
    
    p1[0] = flux1;
    p1[1] = p[1];
    p1[2] = p[2];
    
    p2[0] = flux2;
    p2[1] = p[3];
    p2[2] = p[4];
    
    gaussian(num, x, y, p1);
    gaussian(num, x, y, p2);
}

/* 
Gauss-Hermite polynomials    
      
num: length of x and y
x: wavelength array (Angstrom)
y: flux array (erg/s/cm2/Angstrom)

p[0]: flux (erg/s/cm2)             
p[1]: sigma (Angstrom)                 
p[2]: center (Angstrom)                 
p[3]: skewness                     
p[4]: kurtosis                                              
*/
void gh4(int num, double *x, double *y, double *p)
{
   /* gamma0: flux (erg/s/cm2)                *
    * V0: center (Angstrom)                   *
    * sigma0: sigma (Angstrom)                *
    * xi1: skewness                           *
    * xi2: kurtosis                           */
    
    double gamma0, V0, sigma0, xi1, xi2;
    gamma0 = p[0];
    V0 = p[2];
    sigma0 = p[1];
    xi1 = p[3];
    xi2 = p[4];
     
    double gamma, V, sigma, h3, h4;
    h3 = xi1 / 4.0 / std::pow(3.0, 0.5);
    h4 = (xi2 - 3.0) / 8.0 / std::pow(6.0, 0.5);
    sigma = sigma0 / (1.0 + h4 * std::pow(6.0, 0.5));
    V = V0 - std::pow(3.0, 0.5) * sigma * h3;
    gamma = gamma0 / (1.0 + 0.25 * std::pow(6.0, 0.5) * h4);
    
    double w, L0, L, H_3, H_4;
    double pow6_2 = std::pow(6.0, 0.5), pow2_2 = std::pow(2.0, 0.5), pow24_2 = std::pow(24.0, 0.5);
    L0 = gamma / sigma / std::pow(2.0 * PI, 0.5);
    for (int i = 0; i < num; ++i)
    {
        w = (x[i] - V) / sigma;
        H_3 = 1.0 / pow6_2 * (2.0 * pow2_2 * std::pow(w, 3.0) - 3.0 * pow2_2 * w);
        H_4 = 1.0 / pow24_2 * (4.0 * std::pow(w, 4.0) - 12.0 * std::pow(w, 2.0) + 3.0);
        L = std::exp(-0.5 * w * w);
        y[i] += (1.0 + h3 * H_3 + h4 * H_4) * L0 * L;
    }
}

int checkuniform(int n, double *x, double *y)
{
    /* check whether the step length is uniform in velocity space
     * if uniform return 1, otherwise return 0 */
    int i;
    double dxmin;
    dxmin = std::log(x[1]) - std::log(x[0]);
    for (i = 2; i < n; ++i)
    {
        if ((std::log(x[i]) - std::log(x[i - 1])) < dxmin)
        {
            dxmin = std::log(x[i]) - std::log(x[i - 1]);
        }
    }
    //printf("smallest step length: %f\n", dxmin);

    /* check whether the step length is uniform */
    int status = 1;
    for (i = 2; i < n; i++)
    {
        if (std::fabs((std::log(x[i]) - std::log(x[i - 1])) - dxmin) / dxmin > UNIFORM_LIMIT)
        {
            status = 0;
            break;
        }
    }
    //printf("if step is uniform? (1: yes, 0: no) %i\n", status);
    return status;
}

double smalleststep(int n, double *x, double *y)
{
    /* return the smallest step length is in velocity space */
    int i;
    double dxmin;
    dxmin = std::log(x[1]) - std::log(x[0]);
    for (i = 2; i < n; ++i)
    {
        if ((std::log(x[i]) - std::log(x[i - 1])) < dxmin)
        {
            dxmin = std::log(x[i]) - std::log(x[i - 1]);
        }
    }
    //printf("smallest step length: %f\n", dxmin);
    return dxmin;
}

double largeststep(int n, double *x, double *y)
{
    /* return the largest step length is in velocity space */
    int i;
    double dxmax;
    dxmax = std::log(x[1]) - std::log(x[0]);
    for (i = 2; i < n; ++i)
    {
        if ((std::log(x[i]) - std::log(x[i - 1])) > dxmax)
        {
            dxmax = std::log(x[i]) - std::log(x[i - 1]);
        }
    }
    //printf("largest step length: %f\n", dxmax);
    return dxmax;
}

int convlv_resp_num(double *p, double dlnw, std::string kernel_type)
{
    // fwhm: fwhm/sigma (km/s)
    // shift (km/s)
    // dlnw (): step length
    // m: number of output array
    double fwhm = 0.0, shift = 0.0;
    
    if (kernel_type == "gaussian")
    {
        fwhm = p[1];
        shift = p[2];
    }
    else if (kernel_type == "lorentzian")
    {
        fwhm = p[1];
        shift = p[2];
    }
    else if (kernel_type == "dgaussian")
    {
        fwhm = std::fabs(p[1]) + std::fabs(p[3]);
        shift = std::fabs(p[2]) + std::fabs(p[4]);
    }
    else if (kernel_type == "gh4")
    {
        fwhm = p[1] * 5.0;
        shift = p[2];
    }
    else
    {
        std::cout << "Error! no such kernel type!" << std::endl;
        std::exit(-1);
    }
    
    double c = 3.0e5;
    fwhm = fwhm / c / dlnw;
    shift = shift / c / dlnw;
    if (((int) (fwhm + std::fabs(shift))) == 1)
    {
        std::cout << "fwhm: " << fwhm * c * dlnw << " shift: " << shift * c * dlnw << std::endl;
        std::cout << "Error! array number of the convolve kernel is too small!" << std::endl;
        std::cout << "please make the step length smaller (decrease TEMPLATE_STEP)" << std::endl;
        std::exit(-1);
    }
    int num;
    num = ((int) (fwhm + fabs(shift))) / 2 * CONVOLVE_FACTOR + 1;
    return num;
}

/*
convolvution kernel

p: parameters of kernel (in velocity space, km/s)
m: array length of kernel
kernel_type: type of kernel
*/
void convlv_resp(double *p, double dlnw, int m, double *kernel, std::string kernel_type)
{
    int nhalf, num;
    num = m;
    
    nhalf = (num - 1) / 2;
    double x[num];
    x[0] = 0.0;
    int i;
    for (i = 1; i <= nhalf; ++i)
    {
        x[i] = (double) i;
    }
    for (i = nhalf + 1; i < num; ++i)
    {
        x[i] = (double) (i - num);
    }
    
    /* create kernel */
    double c = 3.0e5;
    for (int i = 0; i < num; ++i) kernel[i] = 0.0;
    if (kernel_type == "gaussian")
    {
        double pnew[3];
        pnew[0] = p[0];
        pnew[1] = p[1] / c / dlnw;
        pnew[2] = p[2] / c / dlnw;
        gaussian(num, x, kernel, pnew);
    }
    else if (kernel_type == "lorentzian")
    {
        double pnew[3];
        pnew[0] = p[0];
        pnew[1] = p[1] / c / dlnw;
        pnew[2] = p[2] / c / dlnw;
        lorentzian(num, x, kernel, pnew);
    }
    else if (kernel_type == "dgaussian")
    {
        double pnew[6];
        pnew[0] = p[0];
        pnew[1] = p[1] / c / dlnw;
        pnew[2] = p[2] / c / dlnw;
        pnew[3] = p[3] / c / dlnw;
        pnew[4] = p[4] / c / dlnw;
        pnew[5] = p[5];
        dgaussian(num, x, kernel, pnew);
    }
    else if (kernel_type == "gh4")
    {
        double pnew[5];
        pnew[0] = p[0];
        pnew[1] = p[1] / c / dlnw;
        pnew[2] = p[2] / c / dlnw;
        pnew[3] = p[3];
        pnew[4] = p[4];
        gh4(num, x, kernel, pnew);
    }
    else
    {
        std::cout << "Error! no such kernel type!" << std::endl;
        std::exit(-1);
    }

}

/* 
please make sure the input array x and y have uniform steps in velocity space,
but the array themselves are in wavelength space!!!
The subroutine do "not" check whether the step is uniform in v-space!!!
The subroutine are used to convolve the array y in velocity space.
n:length of the array x and y
x and y: input array
p: parameters array of kernel (velocity space km/s)
*/ 
void convolve(int n, double *x, double *y, double *yout, double *p, std::string kernel_type)
{
    int i;
    double dxmin = std::log(x[1]) - std::log(x[0]);
    
    /* create convolve kernel */
    int m = convlv_resp_num(p, dxmin, kernel_type);
    double kernel[m];
    convlv_resp(p, dxmin, m, kernel, kernel_type);
    
    /* number for zero padding */
    int num;
    for (i = 0; i < 100; ++i)
    {
        num = std::pow(2, i);
        if (num >= n + m)
        {
            break;
        }
    }
    if (i > 80)
    {
        std::cout << "error! too large array in convolve subroutine" << std::endl;
        std::exit(-1);
    }
    
    /* zero padding of input template */
    double lny[num * 2];
    for (i = 0; i < n; ++i)
    {
        REAL(lny, i) = x[i] * y[i];
        IMAG(lny, i) = 0.0;
    }
    for (i = n; i < num; ++i)
    {
        REAL(lny, i) = 0.0;
        IMAG(lny, i) = 0.0;
    }
    
    /* change kernel to an array with 2xn-elements (complex) */
    int itemp = (m - 1) / 2;
    double respons[num * 2];
    for (i = 0; i <= itemp; ++i)
    {
        REAL(respons, i) = kernel[i];
        IMAG(respons, i) = 0.0;
    }
    for (i = 1; i <= itemp; ++i)
    {
        REAL(respons, num - i) = kernel[m - i];
        IMAG(respons, num - i) = 0.0;
    }
    for (i = itemp + 1; i <= num - itemp - 1; ++i)
    {
        REAL(respons, i) = 0.0;
        IMAG(respons, i) = 0.0;
    }
    
    /* fft */
    int status = 0;
    status = gsl_fft_complex_radix2_forward(lny, 1, num);
    if (status != GSL_SUCCESS)
    {
        std::cout << "Error! in FFT1" << std::endl;
        std::exit(-1);
    }
    
    status = gsl_fft_complex_radix2_forward(respons, 1, num);
    if (status != GSL_SUCCESS)
    {
        std::cout << "Error! in FFT2" << std::endl;
        std::exit(-1);
    }
    
    gsl_complex comp1, comp2, comp3;
    for (i = 0; i < num; i++)
    {
        GSL_SET_COMPLEX(&comp1, REAL(lny, i), IMAG(lny, i));
        GSL_SET_COMPLEX(&comp2, REAL(respons, i), IMAG(respons, i));
        comp3 = gsl_complex_mul(comp1, comp2);
        REAL(lny, i) = GSL_REAL(comp3);
        IMAG(lny, i) = GSL_IMAG(comp3);
    }
    
    status = gsl_fft_complex_radix2_inverse(lny, 1, num);
    if (status != GSL_SUCCESS)
    {
        std::cout << "Error! in FFT3" << std::endl;
        std::exit(-1);
    }
    
    /* put array into yout */
    for (i = 0; i < n; i++)
    {
        yout[i] = REAL(lny, i) / x[i];
    }
}

void correct_redshift(int num, double *wave, double *flux, double *err
        , double *wave1, double *flux1, double *err1, double z)
{
    // wave, flux and err will be replaced by redshift-corrected wave, flux and err
    // num: array length
    // wave: wavelength (Angstrom)
    // flux: flux (erg/s/cm2/A)
    // err: error (erg/s/cm2/A)
    // z: redshift
    for (int i = 0; i < num; ++i)
    {
        wave1[i] = wave[i] / (1.0 + z);
        flux1[i] = flux[i] * (1.0 + z);
        err1[i] = err[i] * (1.0 + z);
    }
}

void ccm_unred(int num, double *wave, double *flux, double ebv, double *funred
        , double r_v)
{
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

    int i;
    double y, y1, fa, fb;
    double x, a, b;
    double a_v, a_lambda;
    for (i = 0; i < num; i++)
    {
        x = 10000.0 / wave[i]; // convert to inverse microns
        // Infrared
        if ((x > 0.3) && (x < 1.1))
        {
            a = 0.574 * pow(x, 1.61);
            b = -0.527 * pow(x, 1.61);
        }
        // Optical/NIR
        else if ((x >= 1.1) && (x < 3.3))
        {
            y = x - 1.82;
            //a = 1.0 + 0.17699 * y - 0.50447 * pow(y, 2)   // Original
            //    - 0.02427 * pow(y, 3) + 0.72085 * pow(y, 4)  // coefficients
            //    + 0.01979 * pow(y, 5) - 0.77530 * pow(y, 6)  // from CCM89
            //    + 0.32999 * pow(y, 7);
            //b = 1.41338 * y + 2.28305 * pow(y, 2)
            //    + 1.07233 * pow(y, 3) - 5.38434 * pow(y, 4)
            //    - 0.62251 * pow(y, 5) + 5.30260 * pow(y, 6)
            //    - 2.09002 * pow(y, 7);
            a = 1.0 + 0.104 * y - 0.609 * pow(y, 2) + 0.701 * pow(y, 3) // O'Donnell
                + 1.137 * pow(y, 4) - 1.718 * pow(y, 5) - 0.827 * pow(y, 6) // (1994)
                + 1.647 * pow(y, 7) - 0.505 * pow(y, 8);
            b = 1.952 * y + 2.908 * pow(y, 2) - 3.989 * pow(y, 3)
                - 7.985 * pow(y, 4) + 11.102 * pow(y, 5) + 5.491 * pow(y, 6)
                - 10.805 * pow(y, 7) + 3.347 * pow(y, 8);
        }
        // Mid-UV
        else if ((x >= 3.3) && (x < 8.0))
        {
            y = x;
            if (y > 5.9)
            {
                y1 = y - 5.9;
                fa = - 0.04473 * pow(y1, 2) - 0.009779 * pow(y1, 3);
                fb = 0.2130 * pow(y1, 2) + 0.1207 * pow(y1, 3);
            }
            else
            {
                fa = 0.0;
                fb = 0.0;
            }
            a = 1.752 - 0.316 * y - (0.104 / (pow(y - 4.67, 2) + 0.341)) + fa;
            b = -3.090 + 1.825 * y + (1.206 / (pow(y - 4.62, 2) + 0.263)) + fb;
        }
        // Far-UV
        else if ((x >= 8.0) && (x <= 11.0))
        {
            y = x - 8.0;
            a = -1.073 - 0.628 * y + 0.137 * pow(y, 2) - 0.070 * pow(y, 3);
            b = 13.670 + 4.257 * y - 0.420 * pow(y, 2) + 0.374 * pow(y, 3);
        }
        else
        {
            printf("caution!!!\n");
            printf("wavelength range %f exceed ccm_unred limitation!!! (%i in wavelength array)\n"
                    , 10000.0 / x, i);
            exit(-1);
        }
        a_v = r_v * ebv;
        a_lambda = a_v * (a + b / r_v);
        funred[i] = flux[i] * pow(10.0, 0.4 * a_lambda);
    }
}
