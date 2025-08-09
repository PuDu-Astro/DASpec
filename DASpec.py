#!/usr/bin/python

"""
Author: Pu Du @ IHEP
Date: 2016.07
Update: 2025.04
"""

import numpy as np
import carray
import swigDASpec
import sys, os
from scipy import optimize

template_PATH = os.getenv("DASpec_TEMPLATE_PATH")

line_centers_air = {
        "Hbeta": 4861.325,
        "Hgamma": 4340.464,
        "[OIII]4959": 4958.911,
        "[OIII]5007": 5006.843,
        "[OIII]4363": 4363.210,
        "HeII": 4685.71,
        "MgII": 2797.963
        }

line_centers_vacuum = {
        "Hbeta": 4862.683,
        "Hgamma": 4341.684,
        "[OIII]4959": 4960.295,
        "[OIII]5007": 5008.240,
        "[OIII]4363": 4364.436,
        "HeII": 4687.02,
        "MgII": 2798.788
        }

fitwindows = [
    [2470, 2625],
    [2675, 2755],
    [2855, 3010],
    [3625, 3645],
    [4170, 4260],
    #[4430, 4770],
    #[5080, 5550],
    [4430, 5550],
    [6050, 6200],
    [6890, 7010]]

fitwindows_continuum = [
    [2470, 2625],
    [2675, 2755],
    [2855, 3010],
    [3625, 3645],
    [4170, 4260],
    #[4430, 4770],
    #[5080, 5550],
    [4430, 5550],
    [6050, 6200],
    [6890, 7010]]

model_name = [
    "powerlaw",
    "balmer_continuum",
    "template_spec",
    "template_spec_reddened",
    "line_gaussian",
    "line_lorentzian",
    "line_dgaussian",
    "line_gh4",
    "ccm_reddening"
]

model_name_p = [
    "powerlaw",
    "balmer_continuum",
    "template_spec_gaussian",
    "template_spec_dgaussian",
    "template_spec_lorentzian",
    "template_spec_gh4",
    "template_spec_reddened_gaussian",
    "template_spec_reddened_dgaussian",
    "template_spec_reddened_lorentzian",
    "template_spec_reddened_gh4",
    "line_gaussian",
    "line_lorentzian",
    "line_dgaussian",
    "line_gh4",
    "ccm_reddening"
]

tie_name = [
    "tie",
    "profile",
    "flux_profile"
]

def str_to_model(arrays):

    """ string array to model """

    model = compcontainer()

    for i in arrays:
        text = 'model.add(' + i + ')'
        #print(text)
        eval(text)
    return model

class array(object):

    """ array object used for transmission with C++ """

    def __init__(self, p):

        """
        initialize object

        p is python array or numpy array
        """

        self.len = len(p)
        self.c_array = carray.newarray(self.len)
        self.py_array = p

        for i in range(self.len):
            carray.setelement(self.c_array, i, p[i])

    def carray(self):
        return self.c_array

    def pyarray(self):
        p = []
        for i in range(self.len):
            p.append(carray.getelement(self.c_array, i))
        return np.array(p)

    def __del__(self):
        carray.delarray(self.c_array)


class compcontainer(object):

    """
    component container

    int npar: number of parameters (all of the models)
    int nmodel: number of models
    component *model: array containing pointers to model

    info: print information of the component

    calc: calculate the model including all of the components
    calc_totpar: calculate the model including all of the components and long par array
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
    type: tie type ("ratio", "offset")
    val: value (ratio or offset)
    """



    def __init__(self):
        self.container = swigDASpec.compcontainer()
        self.comps = []

    def add(self, func):
        self.comps.append(func)       # put it into comps to avoid memory cleanning
        self.container.add(self.comps[-1].func) # put it into c class

    def info(self):
        self.container.info()

    def calc_totpar(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.container.calc_totpar(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.container.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

    def pars2l(self, p):
        ptot = [0.0] * self.container.npar
        cptot = array(ptot)
        cp = array(p)
        self.container.pars2l(cp.carray(), cptot.carray())
        return np.array(cptot.pyarray())

    def parl2s(self, ptot):
        p = [0.0] * self.container.netnpar()
        cp = array(p)
        cptot = array(ptot)
        self.container.parl2s(cptot.carray(), cp.carray())
        return np.array(cp.pyarray())

    def clean(self):
        self.container.clean()
        comps = []

    def addfix(self, c, p, val):
        self.container.addfix(c, p, val)

    def addtie(self, c, p, ct, pt, t, val):
        self.container.addtie(c, p, ct, pt, t, val)

    def addtie_profile(self, c, ct):
        self.container.addtie_profile(c, ct)

    def addtie_flux_profile(self, c, ct, val):
        self.container.addtie_flux_profile(c, ct, val)

    def netnpar(self):
        return self.container.netnpar()

    def calc_comp(self, n, x, par):

        """ calculate component n using parameter """

        n = n - 1

        if n < 0 or n >= len(self.comps):
            print("Error! n is invalid!")
            sys.exit()

        pfit = par

        #print(self.model.comps[n].calc())
        nnp = 0
        if n == 0:
            #print('npar', self.model.comps[n].func.npar)
            p = pfit[0: self.comps[n].func.npar]
        else:
            for i in range(n):
                nnp += self.comps[i].func.npar
            #print(np)
            p = pfit[nnp: nnp + self.comps[n].func.npar]
        #print(p)

        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.comps[n].func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

    def par_comp(self, n, par):

        n = n - 1

        if n < 0 or n >= len(self.comps):
            print("Error! n is invalid!")
            sys.exit()

        pfit = par

        #print(self.model.comps[n].calc())
        nnp = 0
        if n == 0:
            #print('npar', self.model.comps[n].func.npar)
            p = pfit[0: self.comps[n].func.npar]
        else:
            for i in range(n):
                nnp += self.comps[i].func.npar
            #print(np)
            p = pfit[nnp: nnp + self.comps[n].func.npar]
        #print(p)

        return p

class curvefit(object):

    """
    fit model (compcontainer) to the data
    """

    def __init__(self):
        self.curvefit = swigDASpec.curvefit()
        self.model = 0
        self.cx = 0
        self.cy = 0
        self.cerr = 0
        self.cp = 0
        self.fitdone = 0
        self.limits = []

    def set_data(self, x, y, err):
        self.cx = array(x)
        self.cy = array(y)
        self.cerr = array(err)
        self.curvefit.setdata(self.cx.len, self.cx.carray(), self.cy.carray(), self.cerr.carray())

    def set_model(self, m):
        self.model = m
        self.curvefit.setmodel(self.model.container)

    def set_init(self, p):
        self.cp = array(p)
        self.curvefit.setinitp(self.cp.carray())

    def set_limit(self, n, p, limit):
        """
        n: index of parameter
        p: limit
        limit: 0-lower, 1-upper
        """
        self.limits.append([n, p, limit])
        self.curvefit.setlimit(n, p, limit)

    def set_limit_tot(self, p):
        if self.cp.len != len(p) / 2:
            print('error!! number of limits is not equal to the number of parameters!')
            sys.exit()
        for i in range(len(p) / 2):
            #print(i + 1, i * 2, i * 2 + 1)
            self.set_limit(i + 1, p[i * 2], 0)
            self.set_limit(i + 1, p[i * 2 + 1], 1)

    def lmfit(self, nitermax = 200):
        if self.model == 0:
            print("Error! please set model for fitting!")
            sys.exit()
        if self.cp == 0 or self.cp.len != self.model.netnpar():
            print("Error! please set correct initial parameters for fitting!")
            sys.exit()
        if self.cx == 0 or self.cy == 0 or self.cerr == 0:
            print("Error! please set data for fitting!")
            sys.exit()
        self.curvefit.lmfit(nitermax)
        self.fitdone = 1

    def siman(self, ntmax = 50000, ninner = 5000, jump = 0.2,
            ninit = 2000, Tratio = 0.001, delta = 1.0e-6, nstable = 20):
        if self.model == 0:
            print("Error! please set model for fitting!")
            sys.exit()
        if self.cp == 0 or self.cp.len != self.model.netnpar():
            print("Error! please set correct initial parameters for fitting!")
            sys.exit()
        if self.cx == 0 or self.cy == 0 or self.cerr == 0:
            print("Error! please set data for fitting!")
            sys.exit()
        self.curvefit.siman(ntmax, ninner, jump, ninit, Tratio, delta, nstable)
        self.fitdone = 1

    def mix_fit(self, ntmax = 50000, ninner = 200, jump = 0.2,
            ninit = 500, Tratio = 0.01, delta = 1.0e-5, nstable = 20):
        if self.model == 0:
            print("Error! please set model for fitting!")
            sys.exit()
        if self.cp == 0 or self.cp.len != self.model.netnpar():
            print("Error! please set correct initial parameters for fitting!")
            sys.exit()
        if self.cx == 0 or self.cy == 0 or self.cerr == 0:
            print("Error! please set data for fitting!")
            sys.exit()
        self.curvefit.mix_fit(ntmax, ninner, jump, ninit, Tratio, delta, nstable)
        self.fitdone = 1

    def info(self):
        self.curvefit.info()

    def calc(self, x):

        """ calculate model using the fitted parameterr """

        if self.fitdone == 0:
            print("Error! please do the fitting first!")
            sys.exit()

        p = self.par()
        return self.model.calc(x, p)

    def calc_comp(self, n, x):

        """ calculate component n using the fitted parameterr """

        n = n - 1

        if self.fitdone == 0:
            print("Error! please do the fitting first!")
            sys.exit()

        if n < 0 or n >= len(self.model.comps):
            print("Error! n is invalid!")
            sys.exit()

        pfit = self.par_tot()

        #print(self.model.comps[n].calc())
        nnp = 0
        if n == 0:
            #print('npar', self.model.comps[n].func.npar)
            p = pfit[0: self.model.comps[n].func.npar]
        else:
            for i in range(n):
                nnp += self.model.comps[i].func.npar
            #print(np)
            p = pfit[nnp: nnp + self.model.comps[n].func.npar]
        #print(p)

        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.model.comps[n].func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

    def par(self):
        """ return final parameters """
        p = []
        for i in range(self.curvefit.npout):
            p.append(carray.getelement(self.curvefit.pout, i))
        return np.array(p)

    def parerr(self):
        """ return error of parameters """
        p = []
        for i in range(self.curvefit.npout):
            p.append(carray.getelement(self.curvefit.perrout, i))
        return np.array(p)

    def par_tot(self):
        """ return final parameters (tot) """
        p = []
        for i in range(self.curvefit.npout_tot):
            p.append(carray.getelement(self.curvefit.pout_tot, i))
        return np.array(p)

    def parerr_tot(self):
        """ return error of parameters (tot) """
        p = []
        for i in range(self.curvefit.npout_tot):
            p.append(carray.getelement(self.curvefit.perrout_tot, i))
        return np.array(p)

    def chisq(self):
        """ return chisq """
        return self.curvefit.chisq

    def reduced_chisq(self):
        """ return reduced chisq """
        return self.curvefit.reduced_chisq

    def DOF(self):
        """ return DOF """
        return self.curvefit.DOF

    def status(self):
        """ return fit status """
        return self.curvefit.status

    def iternum(self):
        """ return iteration number """
        return self.curvefit.iternum

class line_gaussian(object):

    """
    Gaussian line profile

    center: center of the line

    info: print information of the component

    calc: calculate the component
    p[0]: flux (erg/s/cm2)
    p[1]: FWHM (km/s)
    p[2]: shift (km/s)
    """

    def __init__(self, center = 4861.0):
        self.func = swigDASpec.line_gaussian(center)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class line_dgaussian(object):

    """
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
    """

    def __init__(self, center = 4861.0):
        self.func = swigDASpec.line_dgaussian(center)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class line_lorentzian(object):

    """
    Lorentzian line profile

    center: center of the line

    info: print information of the component

    calc: calculate the component
    p[0]: flux (erg/s/cm2)
    p[1]: FWHM (km/s)
    p[2]: shift (km/s)
    """

    def __init__(self, center = 4861.0):
        self.func = swigDASpec.line_lorentzian(center)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class powerlaw(object):

    """
    power law
    a * (x / c)^b

    ref: c

    info: print information of the component

    calc: calculate the component
    p[0]: flux (erg/s/cm2/A)
    p[1]: power index
    """

    def __init__(self, ref = 5100.0):
        self.func = swigDASpec.powerlaw(ref)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class line_gh4(object):

    """
    Gauss-Hermite polynomials line profile

    center: center of the line

    info: print information of the component

    calc: calculate the component
    p[0]: flux (erg/s/cm2)
    p[1]: sigma (km/s)
    p[2]: shift (km/s)
    p[3]: skewness
    p[4]: kurtosis
    """

    def __init__(self, center = 4861.0):
        self.func = swigDASpec.line_gh4(center)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class template_spec(object):

    """
    template convolved by a certain kernel

    p: parameters of kernel
    """

    cx = 0
    cy = 0

    def __init__(self, filename, kernel = "gaussian", f_llim = 4434.0, f_rlim = 4684.0):
        # read file
        l = open(template_PATH + filename).readlines()
        x = [float(i.split()[0]) for i in l if i[0] != '#']
        y = [float(i.split()[1]) for i in l if i[0] != '#']
        self.cx = array(x)
        self.cy = array(y)
        self.func = swigDASpec.template_spec(self.cx.len, self.cx.carray(), self.cy.carray(),
            kernel, f_llim, f_rlim)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class template_spec_reddened(object):

    """
    reddened template convolved by a certain kernel

    p: parameters of kernel
    """

    cx = 0
    cy = 0

    def __init__(self, filename, kernel = "gaussian", f_llim = 4434.0, f_rlim = 4684.0, r = 3.1):
        # read file
        l = open(template_PATH + filename).readlines()
        x = [float(i.split()[0]) for i in l if i[0] != '#']
        y = [float(i.split()[1]) for i in l if i[0] != '#']
        self.cx = array(x)
        self.cy = array(y)
        self.func = swigDASpec.template_spec_reddened(self.cx.len, self.cx.carray(), self.cy.carray(),
            kernel, f_llim, f_rlim, r)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class balmer_continuum(object):

    """
    balmer continuum

    p[0]: flux at Balmer edge
    p[1]: optical depth of Balmer edge
    """

    def __init__(self):
        self.func = swigDASpec.balmer_continuum()

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [0.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())

class ccm_reddening(object):

    """
    ccm reddening

    p[0]: ebv
    """

    def __init__(self, r = 3.1):
        self.func = swigDASpec.ccm_reddening(r)

    def info(self):
        self.func.info()

    def calc(self, x, p):
        y = [1.0 for i in x]
        cx = array(x)
        cy = array(y)
        cp = array(p)
        self.func.calc(len(x), cx.carray(), cy.carray(), cp.carray())
        return np.array(cy.pyarray())


def test():

    import pyfits
    from pyastrolib import astro
    import matplotlib.pyplot as plt

    fit = pyfits.open("spSpec-52368-0881-064.fit")
    #print(fit[0].header)
    wave0 = fit[0].header["CRVAL1"]
    nwave = fit[0].header["NAXIS1"]
    dwave = fit[0].header["CD1_1"]
    wave = wave0 + dwave * np.arange(nwave)
    wave = 10.0**wave
    data = fit[0].data
    flux = data[0]
    err = data[2]

    index = np.where(err > 0)
    wave = wave[index[0]]
    flux = flux[index[0]]
    err = err[index[0]]
    (wave, flux, err) = np.array((wave, flux, err), dtype = np.double)

    #astro.ccm_unred(wave, flux, 0.112 - 0.085)
    z = 0.153375
    wave = wave / (1.0 + z)
    flux = flux * (1.0 + z)
    err = err * (1.0 + z)

    index = np.where(#((wave >= 2470) & (wave <= 2625)) |
            #((wave >= 2675) & (wave <= 2755)) |
            #((wave >= 2855) & (wave <= 3010)) |
            #((wave >= 3625) & (wave <= 3645)) |
            #((wave >= 4170) & (wave <= 4260)) |
            #((wave >= 4430) & (wave <= 4770)) |
            #((wave >= 5080) & (wave <= 5550)) |
            ((wave >= 4430) & (wave <= 5550)))# |
            #((wave >= 6050) & (wave <= 6200)) |
            #((wave >= 6890) & (wave <= 7010)) )

    wave1 = wave[index[0]]
    flux1 = flux[index[0]]
    err1 = err[index[0]]

    model = compcontainer()
    model.add(powerlaw())
    #model.add(balmer_continuum())
    model.add(template_spec("fetemplate_no3"))
    model.add(line_dgaussian(4861))
    model.add(line_gaussian(4959))
    model.add(line_gaussian(5007))
    model.addtie_flux_profile(5, 4, 3.0)
    model.info()
    #model.comps[0].info()

    fit = curvefit()
    fit.set_model(model)
    fit.set_data(wave1, flux1, err1)
    #fit.set_init([1.0, -2.0, 1.0, 0.2, 100.0, 100.0, 0.0, 1.0, 1000.0, 0.0, 1.0, 200.0, 0, 1, 200, 0, 1, 200, 0])
    fit.set_init([0.79978568690512, -0.067457407191308,# 3.520216701612777, 0.1,
        5.85184328147245, 3000.48748920527652, -800.88713428317556,
        0, 1000.0, 0, 3000, 1000, 0.2, 1, 500, 0])
    #fit.set_limit(4, 0.01, 0)
    #fit.set_limit(4, 2.00, 1)
    #fit.set_limit(6, 10.0, 0)
    #fit.set_limit(6, 10000.0, 1)
    #fit.set_limit(7, -10000.0, 0)
    #fit.set_limit(7, 10000.0, 1)

    #fit.lmfit()

    #print(fit.par())
    #print(fit.parerr())
    #print(fit.par_tot())
    #print(fit.parerr_tot())
    #y = fit.calc_comp(1, [1, 2, 3])
    #print(fit.parerr())

    fit.set_limit(1, 0, 0)
    fit.set_limit(1, 1000, 1)
    fit.set_limit(2, -3, 0)
    fit.set_limit(2, 0, 1)
    #fit.set_limit(3, 0, 0)
    #fit.set_limit(3, 100, 1)
    #fit.set_limit(4, 0.01, 0)
    #fit.set_limit(4, 0.5, 1)
    fit.set_limit(3, 0.0, 0)
    fit.set_limit(3, 1000, 1)
    fit.set_limit(4, 100.0, 0)
    fit.set_limit(4, 2000, 1)
    fit.set_limit(5, -2000.0, 0)
    fit.set_limit(5, 2000, 1)
    fit.set_limit(6, 0.0, 0)
    fit.set_limit(6, 10000, 1)
    fit.set_limit(7, 1.0, 0)
    fit.set_limit(7, 5000, 1)
    fit.set_limit(8, -2000.0, 0)
    fit.set_limit(8, 2000, 1)
    fit.set_limit(9, 1.0, 0)
    fit.set_limit(9, 5000, 1)
    fit.set_limit(10, -2000.0, 0)
    fit.set_limit(10, 2000, 1)
    fit.set_limit(11, 0.0, 0)
    fit.set_limit(11, 1.0, 1)
    fit.set_limit(12, 0.0, 0)
    fit.set_limit(12, 1e4, 1)
    fit.set_limit(13, 1.0, 0)
    fit.set_limit(13, 5000, 1)
    fit.set_limit(14, -2000.0, 0)
    fit.set_limit(14, 2000, 1)

    #fit.siman()
    fit.mix_fit()
    #fit.lmfit()
    print(fit.par())
    print(fit.parerr())
    #print fit.chisq()

    #fit.lmfit()
    #print(fit.par())
    #print(fit.parerr())

    plt.plot(wave, flux)
    plt.plot(wave, fit.calc(wave))
    plt.plot(wave, fit.calc_comp(1, wave))
    plt.plot(wave, fit.calc_comp(2, wave))
    plt.plot(wave, fit.calc_comp(3, wave))
    plt.plot(wave, fit.calc_comp(4, wave))
    plt.plot(wave, fit.calc_comp(5, wave))
    #plt.plot(wave, fit.calc_comp(6, wave))
    #plt.show()



    #a = compcontainer()
    #a.add(line_gaussian())
    #a.add(template_spec("fetemplate_no3"))
    #a.add(template_spec_reddened("fetemplate_no3"))
    #a.info()

    #x = np.linspace(4500.0, 5200.0, 1000)
    #da = line_gaussian().calc(x, [1.0, 1000.0, 0.0])

    #b = curvefit()
    #b.set_model(a)
    #b.set_init([10.0, 100.0, -100.0])
    #b.set_data(x, da, np.ones(len(x)))
    #b.info()
    #b.lmfit()
    #b.info()

if __name__ == "__main__":
    test()
