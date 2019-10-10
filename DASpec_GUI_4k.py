#!/usr/bin/python

"""
Author: Pu Du @ IHEP
Date: 2016.07
Update: 2019.10
"""

import sys
import Tkinter
import tkFileDialog
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib as mpl
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
import DASpec
import numpy as np
import bwidget

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def cal_scale(flux):
    median = np.median(flux)
    return 10.0**np.ceil(np.log10(median))

class GUI(Tkinter.Frame):

    """ DASpec GUI """

    def __init__(self):
        self.windows = []
        self.fitwindow_info = []
        self.figfitwindow = []
        self.fitwindow = []
        self.models = []
        self.model_info = []
        self.fix_info = []
        self.fix = []
        self.tie_info = []
        self.tie = []
        self.index = -1

        #matplotlib.use("TkAgg")
        self.parent = Tkinter.Tk()
        self.parent.tk.call('tk', 'scaling', 2.0)
        #self.parent.geometry("640x550+350+0")
        self.parent.geometry("1280x1100+700+0")
        #Tkinter.Frame.__init__(self, self.parent)
        self.initUI()


        if len(sys.argv) >= 3:
            if sys.argv[1] == '-s':
                self.specfile = sys.argv[2]
                self.outputfile = open(self.specfile + '.out', 'a')
                self.onOpen()
            elif sys.argv[1] == '-b':
                self.listfile = sys.argv[2]
                self.outputfile = open(self.listfile + '.out', 'a')
                l = open(self.listfile).readlines()
                self.speclist = [i.split('\n')[0] for i in l]
                self.index = 0
                self.specfile = self.speclist[self.index]
                self.onOpen()
            else:
                print 'please use -s or -b'
                sys.exit()
        
        if len(sys.argv) == 5:
            if sys.argv[3] == '-m':
                self.set_model_from_file(sys.argv[4])



    def initmodel(self, wave_lim1, wave_lim2):
        self.models.append(["powerlaw", 5100.0])
        self.models.append(["balmer_continuum"])
        self.models.append(["template_spec_gaussian", "fetemplate_no3", 4434.0, 4684.0])
        #for i in DASpec.line_centers_air:
        #    #print i, DASpec.line_centers_air[i]
        #    if DASpec.line_centers_air[i] >= wave_lim1 and DASpec.line_centers_air[i] <= wave_lim2:
        #        self.models.append(['line_gaussian', DASpec.line_centers_air[i]])
        #print self.models

    def update_model_individual(self, i):
        if self.models[i][0] == "powerlaw":
            self.models[i][0:-2] = ["powerlaw", 5100.0]
        if self.models[i][0] == "balmer_continuum":
            self.models[i][0:-2] = ["balmer_continuum"]
        if self.models[i][0] == "template_spec_gaussian":
            self.models[i][0:-2] = ["template_spec_gaussian", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_dgaussian":
            self.models[i][0:-2] = ["template_spec_dgaussian", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_lorentzian":
            self.models[i][0:-2] = ["template_spec_lorentzian", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_gh4":
            self.models[i][0:-2] = ["template_spec_gh4", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_reddened_gaussian":
            self.models[i][0:-2] = ["template_spec_reddened_gaussian", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "template_spec_reddened_dgaussian":
            self.models[i][0:-2] = ["template_spec_reddened_dgaussian", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "template_spec_reddened_lorentzian":
            self.models[i][0:-2] = ["template_spec_reddened_lorentzian", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "template_spec_reddened_gh4":
            self.models[i][0:-2] = ["template_spec_reddened_gh4", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "line_gaussian":
            self.models[i][0:-2] = ['line_gaussian', 4861.0]
        if self.models[i][0] == "line_lorentzian":
            self.models[i][0:-2] = ['line_lorentzian', 4861.0]
        if self.models[i][0] == "line_dgaussian":
            self.models[i][0:-2] = ['line_dgaussian', 4861.0]
        if self.models[i][0] == "line_gh4":
            self.models[i][0:-2] = ['line_gh4', 4861.0]
        if self.models[i][0] == "ccm_reddening":
            self.models[i][0:-2] = ['ccm_reddening', 3.1]

    def add_model_individual(self, i):
        if self.models[i][0] == "powerlaw":
            self.models[i] = ["powerlaw", 5100.0]
        if self.models[i][0] == "balmer_continuum":
            self.models[i] = ["balmer_continuum"]
        if self.models[i][0] == "template_spec_gaussian":
            self.models[i] = ["template_spec_gaussian", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_dgaussian":
            self.models[i] = ["template_spec_dgaussian", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_lorentzian":
            self.models[i] = ["template_spec_lorentzian", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_gh4":
            self.models[i] = ["template_spec_gh4", "fetemplate_no3", 4434.0, 4684.0]
        if self.models[i][0] == "template_spec_reddened_gaussian":
            self.models[i] = ["template_spec_reddened_gaussian", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "template_spec_reddened_dgaussian":
            self.models[i] = ["template_spec_reddened_dgaussian", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "template_spec_reddened_lorentzian":
            self.models[i] = ["template_spec_reddened_lorentzian", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "template_spec_reddened_gh4":
            self.models[i] = ["template_spec_reddened_gh4", "fetemplate_no3", 4434.0, 4684.0, 3.1]
        if self.models[i][0] == "line_gaussian":
            self.models[i] = ['line_gaussian', 4861.0]
        if self.models[i][0] == "line_lorentzian":
            self.models[i] = ['line_lorentzian', 4861.0]
        if self.models[i][0] == "line_dgaussian":
            self.models[i] = ['line_dgaussian', 4861.0]
        if self.models[i][0] == "line_gh4":
            self.models[i] = ['line_gh4', 4861.0]
        if self.models[i][0] == "ccm_reddening":
            self.models[i] = ['ccm_reddening', 3.1]

    def set_par0(self):
        for i in xrange(len(self.models)):
            if self.models[i][0] == "powerlaw":
                self.models[i].append([1.0, -2.0])
            if self.models[i][0] == "balmer_continuum":
                self.models[i].append([1.0, 0.05])
            if self.models[i][0] == "template_spec_gaussian":
                self.models[i].append([1.0, 200.0, 0.0])
            if self.models[i][0] == "template_spec_dgaussian":
                self.models[i].append([1.0, 200.0, 0.0, 500.0, 0.0, 0.5])
            if self.models[i][0] == "template_spec_lorentzian":
                self.models[i].append([1.0, 200.0, 0.0])
            if self.models[i][0] == "template_spec_gh4":
                self.models[i].append([1.0, 200.0, 0.0, 0.2, 0.2])
            if self.models[i][0] == "template_spec_reddened_gaussian":
                self.models[i].append([1.0, 200.0, 0.0, 0.0])
            if self.models[i][0] == "template_spec_reddened_dgaussian":
                self.models[i].append([1.0, 200.0, 0.0, 500.0, 0.0, 0.5, 0.0])
            if self.models[i][0] == "template_spec_reddened_lorentzian":
                self.models[i].append([1.0, 200.0, 0.0, 0.0])
            if self.models[i][0] == "template_spec_reddened_gh4":
                self.models[i].append([1.0, 200.0, 0.0, 0.2, 0.2, 0.0])
            if self.models[i][0] == "line_gaussian":
                self.models[i].append([1.0, 200.0, 0.0])
            if self.models[i][0] == "line_lorentzian":
                self.models[i].append([1.0, 200.0, 0.0])
            if self.models[i][0] == "line_dgaussian":
                self.models[i].append([1.0, 200.0, 0.0, 500.0, 0.0, 0.5])
            if self.models[i][0] == "line_gh4":
                self.models[i].append([1.0, 200.0, 0.0, 0.2, 0.2])
            if self.models[i][0] == "ccm_reddening":
                self.models[i].append([0.0])
        #print self.models

    def set_limit(self):
        for i in xrange(len(self.models)):
            if self.models[i][0] == "powerlaw":
                self.models[i].append([0.0, 1.0e2, -4.0, 0.0])
            if self.models[i][0] == "balmer_continuum":
                self.models[i].append([0.0, 1.0e2, 0.01, 0.5])
            if self.models[i][0] == "template_spec_gaussian":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0])
            if self.models[i][0] == "template_spec_dgaussian":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0])
            if self.models[i][0] == "template_spec_lorentzian":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0])
            if self.models[i][0] == "template_spec_gh4":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0])
            if self.models[i][0] == "template_spec_reddened_gaussian":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 2.0])
            if self.models[i][0] == "template_spec_reddened_dgaussian":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0, 0.0, 2.0])
            if self.models[i][0] == "template_spec_reddened_lorentzian":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 2.0])
            if self.models[i][0] == "template_spec_reddened_gh4":
                self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0, 0.0, 2.0])
            if self.models[i][0] == "line_gaussian":
                self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0])
            if self.models[i][0] == "line_lorentzian":
                self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0])
            if self.models[i][0] == "line_dgaussian":
                self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0])
            if self.models[i][0] == "line_gh4":
                self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0])
            if self.models[i][0] == "ccm_reddening":
                self.models[i].append([0.0, 2.0])

    def update_par0_individual(self, i):
        if self.models[i][0] == "powerlaw":
            self.models[i][-2] = [1.0, -2.0]
        if self.models[i][0] == "balmer_continuum":
            self.models[i][-2] = [1.0, 0.05]
        if self.models[i][0] == "template_spec_gaussian":
            self.models[i][-2] = [1.0, 200.0, 0.0]
        if self.models[i][0] == "template_spec_lorentzian":
            self.models[i][-2] = [1.0, 200.0, 0.0]
        if self.models[i][0] == "template_spec_dgaussian":
            self.models[i][-2] = [1.0, 200.0, 0.0, 500.0, 0.0, 0.5]
        if self.models[i][0] == "template_spec_gh4":
            self.models[i][-2] = [1.0, 200.0, 0.0, 0.2, 0.2]
        if self.models[i][0] == "template_spec_reddened_gaussian":
            self.models[i][-2] = [1.0, 200.0, 0.0, 0.0]
        if self.models[i][0] == "template_spec_reddened_dgaussian":
            self.models[i][-2] = [1.0, 200.0, 0.0, 500.0, 0.0, 0.5, 0.0]
        if self.models[i][0] == "template_spec_reddened_lorentzian":
            self.models[i][-2] = [1.0, 200.0, 0.0, 0.0]
        if self.models[i][0] == "template_spec_reddened_gh4":
            self.models[i][-2] = [1.0, 200.0, 0.0, 0.2, 0.2, 0.0]
        if self.models[i][0] == "line_gaussian":
            self.models[i][-2] = [1.0, 200.0, 0.0]
        if self.models[i][0] == "line_lorentzian":
            self.models[i][-2] = [1.0, 200.0, 0.0]
        if self.models[i][0] == "line_dgaussian":
            self.models[i][-2] = [1.0, 200.0, 0.0, 500.0, 0.0, 0.5]
        if self.models[i][0] == "line_gh4":
            self.models[i][-2] = [1.0, 200.0, 0.0, 0.2, 0.2]
        if self.models[i][0] == "ccm_reddening":
            self.models[i][-2] = [0.0]
        #print self.models

    def add_par0_individual(self, i):
        if self.models[i][0] == "powerlaw":
            self.models[i].append([1.0, -2.0])
        if self.models[i][0] == "balmer_continuum":
            self.models[i].append([1.0, 0.05])
        if self.models[i][0] == "template_spec_gaussian":
            self.models[i].append([1.0, 200.0, 0.0])
        if self.models[i][0] == "template_spec_lorentzian":
            self.models[i].append([1.0, 200.0, 0.0])
        if self.models[i][0] == "template_spec_dgaussian":
            self.models[i].append([1.0, 200.0, 0.0, 500.0, 0.0, 0.5])
        if self.models[i][0] == "template_spec_gh4":
            self.models[i].append([1.0, 200.0, 0.0, 0.2, 0.2])
        if self.models[i][0] == "template_spec_reddened_gaussian":
            self.models[i].append([1.0, 200.0, 0.0, 0.0])
        if self.models[i][0] == "template_spec_reddened_dgaussian":
            self.models[i].append([1.0, 200.0, 0.0, 500.0, 0.0, 0.5, 0.0])
        if self.models[i][0] == "template_spec_reddened_lorentzian":
            self.models[i].append([1.0, 200.0, 0.0, 0.0])
        if self.models[i][0] == "template_spec_reddened_gh4":
            self.models[i].append([1.0, 200.0, 0.0, 0.2, 0.2, 0.0])
        if self.models[i][0] == "line_gaussian":
            self.models[i].append([1.0, 200.0, 0.0])
        if self.models[i][0] == "line_lorentzian":
            self.models[i].append([1.0, 200.0, 0.0])
        if self.models[i][0] == "line_dgaussian":
            self.models[i].append([1.0, 200.0, 0.0, 500.0, 0.0, 0.5])
        if self.models[i][0] == "line_gh4":
            self.models[i].append([1.0, 200.0, 0.0, 0.2, 0.2])
        if self.models[i][0] == "ccm_reddening":
            self.models[i].append([0.0])

    def update_limit_individual(self, i):
        if self.models[i][0] == "powerlaw":
            self.models[i][-1] = [0.0, 1.0e2, -4.0, 0.0]
        if self.models[i][0] == "balmer_continuum":
            self.models[i][-1] = [0.0, 1.0e2, 0.01, 0.5]
        if self.models[i][0] == "template_spec_gaussian":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0]
        if self.models[i][0] == "template_spec_dgaussian":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0]
        if self.models[i][0] == "template_spec_lorentzian":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0]
        if self.models[i][0] == "template_spec_gh4":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0]
        if self.models[i][0] == "template_spec_reddened_gaussian":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 2.0]
        if self.models[i][0] == "template_spec_reddened_dgaussian":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0, 0.0, 2.0]
        if self.models[i][0] == "template_spec_reddened_lorentzian":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 2.0]
        if self.models[i][0] == "template_spec_reddened_gh4":
            self.models[i][-1] = [0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0, 0.0, 2.0]
        if self.models[i][0] == "line_gaussian":
            self.models[i][-1] = [0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0]
        if self.models[i][0] == "line_lorentzian":
            self.models[i][-1] = [0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0]
        if self.models[i][0] == "line_dgaussian":
            self.models[i][-1] = [0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0]
        if self.models[i][0] == "line_gh4":
            self.models[i][-1] = [0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0]
        if self.models[i][0] == "ccm_reddening":
            self.models[i][-1] = [0.0, 2.0]

        #print self.models

    def add_limit_individual(self, i):
        if self.models[i][0] == "powerlaw":
            self.models[i].append([0.0, 1.0e2, -4.0, 0.0])
        if self.models[i][0] == "balmer_continuum":
            self.models[i].append([0.0, 1.0e2, 0.01, 0.5])
        if self.models[i][0] == "template_spec_gaussian":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0])
        if self.models[i][0] == "template_spec_dgaussian":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0])
        if self.models[i][0] == "template_spec_lorentzian":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0])
        if self.models[i][0] == "template_spec_gh4":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0])
        if self.models[i][0] == "template_spec_reddened_gaussian":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 2.0])
        if self.models[i][0] == "template_spec_reddened_dgaussian":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0, 0.0, 2.0])
        if self.models[i][0] == "template_spec_reddened_lorentzian":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 2.0])
        if self.models[i][0] == "template_spec_reddened_gh4":
            self.models[i].append([0.0, 1.0e4, 100.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0, 0.0, 2.0])
        if self.models[i][0] == "line_gaussian":
            self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0])
        if self.models[i][0] == "line_lorentzian":
            self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0])
        if self.models[i][0] == "line_dgaussian":
            self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0, 100.0, 10000.0, -2000.0, 2000.0, 0.0, 1.0])
        if self.models[i][0] == "line_gh4":
            self.models[i].append([0.0, 1.0e4, 1.0, 10000.0, -2000.0, 2000.0, -5.0, 5.0, -5.0, 5.0])
        if self.models[i][0] == "ccm_reddening":
            self.models[i].append([0.0, 2.0])


    def initUI(self):
        self.parent.title("spectrum")

        menubar = Tkinter.Menu(self.parent)
        self.parent.config(menu = menubar)

        fileMenu = Tkinter.Menu(menubar)
        fileMenu.add_command(label = "single", command = self.single_spectrum)
        fileMenu.add_command(label = "batch", command = self.batch_spectra)
        fileMenu.add_command(label = "Exit", command = self.parent.quit)
        menubar.add_cascade(label = "Spectrum", menu = fileMenu)

        fileMenu = Tkinter.Menu(menubar)
        fileMenu.add_command(label = "Load", command = self.set_model_from_text)
        menubar.add_cascade(label = "Set model", menu = fileMenu)

        fileMenu = Tkinter.Menu(menubar)
        fileMenu.add_command(label = "About DASpec", command = self.authorinfo)
        menubar.add_cascade(label = "Info", menu = fileMenu)

    def authorinfo(self):
        t = Tkinter.Toplevel(self.parent)
        t.title("About")
        #t.geometry("285x200+350+350")
        t.geometry("570x400+700+700")
        l = Tkinter.Label(t, text = "Decomposition of AGN Spectrum (DASpec)")
        l.grid(row = 0, column = 0)
        l = Tkinter.Label(t, text = "Version 0.8")
        l.grid(row = 1, column = 0)
        l = Tkinter.Label(t, text = "")
        l.grid(row = 2, column = 0)
        l = Tkinter.Label(t, text = "Pu Du")
        l.grid(row = 3, column = 0)
        l = Tkinter.Label(t, text = "Institute of High Energy Physics")
        l.grid(row = 4, column = 0)
        l = Tkinter.Label(t, text = "Chinese Academy of Sciences")
        l.grid(row = 5, column = 0)
        l = Tkinter.Label(t, text = "")
        l.grid(row = 6, column = 0)
        l = Tkinter.Label(t, text = "July 2019")
        l.grid(row = 7, column = 0)
        l = Tkinter.Label(t, text = "All rights reserved.")
        l.grid(row = 8, column = 0)

    def single_spectrum(self):
        dlg = tkFileDialog.Open(self.parent, initialdir = ".")
        self.specfile = dlg.show()
        self.outputfile = open(self.specfile + '.out', 'a')
        self.onOpen()

    def batch_spectra(self):
        dlg = tkFileDialog.Open(self.parent, initialdir = ".")
        self.listfile = dlg.show()
        self.outputfile = open(self.listfile + '.out', 'a')
        l = open(self.listfile).readlines()
        self.speclist = [i.split('\n')[0] for i in l]
        self.index = 0
        self.specfile = self.speclist[self.index]
        self.onOpen()

    def selectallmodel(self):
        for i in self.model_info:
            i[1].select()

    def deselectallmodel(self):
        for i in self.model_info:
            i[1].deselect()

    def addmodel(self):
        #print self.addmodel_info
        for j in xrange(len(self.addmodel_info)):
            #print self.model_info[i][-1][j].get()
            if self.addmodel_info[j].get() == 1:
                #print i, j
                #itar = i
                jtar = j
                self.addmodel_info[j].set(0)

        self.models.append([DASpec.model_name_p[jtar]])

        #self.update_model_individual(-1)
        #self.update_par0_individual(-1)
        #self.update_limit_individual(-1)

        self.add_model_individual(-1)
        self.add_par0_individual(-1)
        self.add_limit_individual(-1)

        #print self.model_info
        #for i in self.model_info:
        #    i[1].grid_forget()
        #    i[2].grid_forget()
        #    for j in xrange(len(i) - 7):
        #        i[j + 4].grid_forget()
        #    for j in i[-3]:
        #        j.grid_forget()
        #    for j in i[-2]:
        #        j.grid_forget()
        #    for j in i[-1]:
        #        j.grid_forget()

        #self.model_info = []

        iwin1 = 1 + 3 * (len(self.models) - 1)
        #for iwin in xrange(len(self.models)):
        for iwin in [len(self.models) - 1]:
            self.model_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[1], text = str(iwin + 1),
                variable = self.model_info[iwin][0])
            self.model_info[iwin].append(c1)
            c1.grid(row = iwin1, column = 0, sticky = Tkinter.W)
            m = Tkinter.Menubutton(self.windows[1], text = self.models[iwin][0], width = 22)
            self.model_info[iwin].append(m)
            m.grid(row = iwin1, column = 1)
            m.menu = Tkinter.Menu(m)
            m["menu"] = m.menu
            self.model_info[iwin].append([])
            #print self.model_info
            for i in DASpec.model_name_p:
                var = Tkinter.IntVar()
                self.model_info[iwin][3].append(var)
                m.menu.add_checkbutton(label = i, variable = var, command = self.updatemodel)
            #print self.model_info
            col = 2
            #print self.models[iwin]
            for ipar in xrange(len(self.models[iwin]) - 3):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][col - 1]))
                col += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-2][ipar]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2 + 1]))
                col += 1
            iwin1 += 1

    def check_model_parlimit(self):
        for i in xrange(len(self.models)):
            for j in xrange(len(self.models[i][-2])):
                if self.models[i][-1][j * 2] <= self.models[i][-2][j] <= self.models[i][-1][j * 2 + 1]:
                    pass
                else:
                    print 'Warning!  par ', j + 1, ' in comp ', i + 1, ' without par limits!'

    def addmodel_from_known(self, modelname, modelpar, par):
        #print self.addmodel_info
        #for j in xrange(len(self.addmodel_info)):
            #print self.model_info[i][-1][j].get()
        #    if self.addmodel_info[j].get() == 1:
                #print i, j
                #itar = i
        #        jtar = j
        #        self.addmodel_info[j].set(0)

        #self.models.append([DASpec.model_name_p[jtar]])

        if modelname == 'template_spec' or modelname == 'template_spec_reddened':
            modelname = modelname + '_' + modelpar[1]
            del modelpar[1]

        self.models.append([modelname])


        #self.update_model_individual(-1)
        #self.update_par0_individual(-1)
        #self.update_limit_individual(-1)

        self.add_model_individual(-1)
        self.add_par0_individual(-1)
        self.add_limit_individual(-1)



        #print self.models

        #print '-' * 40

        if self.models[-1][0] != 'balmer_continuum':
            for i in xrange(len(modelpar)):
                self.models[-1][i + 1] = modelpar[i]
            self.models[-1][-2] = par
        else:
            #self.models[-1][1] = ['balmer_continuum']
            self.models[-1][-2] = par

        #print self.models

        self.check_model_parlimit()

        #print '#' * 40

        #sys.exit()

        #print self.model_info
        #for i in self.model_info:
        #    i[1].grid_forget()
        #    i[2].grid_forget()
        #    for j in xrange(len(i) - 7):
        #        i[j + 4].grid_forget()
        #    for j in i[-3]:
        #        j.grid_forget()
        #    for j in i[-2]:
        #        j.grid_forget()
        #    for j in i[-1]:
        #        j.grid_forget()

        #self.model_info = []

        iwin1 = 1 + 3 * (len(self.models) - 1)
        #for iwin in xrange(len(self.models)):
        for iwin in [len(self.models) - 1]:
            self.model_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[1], text = str(iwin + 1),
                variable = self.model_info[iwin][0])
            self.model_info[iwin].append(c1)
            c1.grid(row = iwin1, column = 0, sticky = Tkinter.W)
            m = Tkinter.Menubutton(self.windows[1], text = self.models[iwin][0], width = 22)
            self.model_info[iwin].append(m)
            m.grid(row = iwin1, column = 1)
            m.menu = Tkinter.Menu(m)
            m["menu"] = m.menu
            self.model_info[iwin].append([])
            #print self.model_info
            for i in DASpec.model_name_p:
                var = Tkinter.IntVar()
                self.model_info[iwin][3].append(var)
                m.menu.add_checkbutton(label = i, variable = var, command = self.updatemodel)
            #print self.model_info
            col = 2
            #print self.models[iwin]
            for ipar in xrange(len(self.models[iwin]) - 3):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][col - 1]))
                col += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-2][ipar]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2 + 1]))
                col += 1
            iwin1 += 1

    def delmodel(self):
        if self.models != []:
            i = self.model_info[-1]
            i[1].grid_forget()
            i[2].grid_forget()
            for j in xrange(len(i) - 7):
                i[j + 4].grid_forget()
            for j in i[-3]:
                j.grid_forget()
            for j in i[-2]:
                j.grid_forget()
            for j in i[-1]:
                j.grid_forget()
            del self.model_info[-1]
            del self.models[-1]
            return 1
        else:
            #print 'already no models!'
            return 0

    def model_useresult(self):
        try:
            if self.curvefit.fitdone == 1:
                par_tot = self.curvefit.par_tot()
                #print len(par_tot)
                #parnum = []
                num = 0
                for i in self.model_info:
                    if i[0].get():
                        #parnum.append(len(i[-3]))
                        for j in xrange(len(i[-3])):
                            i[-3][j].delete(0, Tkinter.END)
                            i[-3][j].insert(0, '%.5e' % (par_tot[num]))
                            num += 1
            else:
                print 'please do the fitting first!'
        except AttributeError as e:
            print 'please do the fitting first!'


    def set_model_from_text(self):

        # print self.models
        # print self.model_info
        # print self.fix
        # print self.fix_info
        # print self.tie
        # print self.tie_info
        # print self.addmodel_info
        # print self.index

        # raw_input("")
        # sys.exit()

        dlg = tkFileDialog.Open(self.parent, initialdir = ".")
        modelfile = dlg.show()
        print 'load model from the last fit in ', modelfile

        self.set_model_from_file(modelfile)

    def set_model_from_file(self, modelfile):
        l = open(modelfile).readlines()
        reduced_l = self.output_reduce(l)

        while 1:
            if self.delmodel() == 0:
                break

        while 1:
            if self.deltie() == 0:
                break
        
        while 1:
            if self.delfix() == 0:
                break


        for i in xrange(len(reduced_l)):
            if reduced_l[i][0] == '#' and reduced_l[i].split()[1] == 'window:':
                iwin = i + 1
            if reduced_l[i][0] == '#' and reduced_l[i].split()[1] == 'model:':
                imodel_start = i + 1
            if reduced_l[i][0] == '#' and reduced_l[i].split()[1] == 'fix:':
                ifix_start = i + 1
                imodel_end = i
            if reduced_l[i][0] == '#' and reduced_l[i].split()[1] == 'tie:':
                itie_start = i + 1
                ifix_end = i
            if reduced_l[i][0] == '#' and reduced_l[i].split()[1] == 'reduced':
                itie_end = i

        #print imodel_start, imodel_end, ifix_start, ifix_end, itie_start, itie_end

        wins = [i.replace(']', '').split() for i in reduced_l[iwin].replace('\n', '').split('[')[1:]]
        #print wins
        #sys.exit()
        for i in xrange(len(wins)):
            self.addwin_from_known(wins[i][0], wins[i][1])
        self.updatewin()



        if imodel_start != imodel_end:
            models = [i for i in reduced_l[imodel_start:imodel_end]]
        else:
            models = []

        if ifix_start != ifix_end:
            fixes = [i for i in reduced_l[ifix_start:ifix_end]]
        else:
            fixes = []

        if itie_start != itie_end:
            ties = [i for i in reduced_l[itie_start:itie_end]]
        else:
            ties = []

        pars = [i for i in reduced_l if "par of comp" in i]

        # print models
        # print fixes
        # print ties
        # print pars

        for i in xrange(len(models)):
            modelname = models[i].split()[1].split("(")[0]
            modelpar = models[i].split()[1].split("(")[1].split(")")[0].split(",")
            modelpar = [j.replace("'", "") for j in modelpar]
            modelpar2 = []
            for j in modelpar:
                if self.is_number(j):
                    #print j, 'yes'
                    modelpar2.append(float(j))
                else:
                    #print j, 'no'
                    modelpar2.append(j)
            modelpar = modelpar2

            par = [float(j) for j in pars[i].split(":")[1].split()]
            print modelname, modelpar, par
            self.addmodel_from_known(modelname, modelpar, par)
        self.selectallmodel()

        if len(ties) != 0:
            for i in xrange(len(ties)):
                temp = ties[i]
    
                #print temp
                if len(temp.split()) == 8:
                    tietype = ''
                    temp = temp.replace("->", "")
                    temp.replace('ratio', '0')
                    temp.replace('offset', '1')
    
                    tiepar = []
                    for j in xrange(len(temp.split()) - 1):
                        #print j
                        tiepar.append(temp.split()[j + 1].split(':')[1])
                else:
                    tietype = temp.split()[1]
                    temp = temp.replace("->", "")
                    #print temp
    
                    tiepar = []
                    for j in xrange(len(temp.split()) - 2):
                        tiepar.append(temp.split()[j + 2].split(':')[1])
    
                #print tietype, tiepar
                self.addtie_from_known(tietype, tiepar)
            
            self.selectalltie()
            self.updatetie()

        if len(fixes) != 0:
            for i in xrange(len(fixes)):
                fixpar = []
                for j in xrange(len(fixes[i].split()) - 1):
                    fixpar.append(fixes[i].split()[j + 1].split(':')[1])
                #print fixpar
                self.addfix_from_known(fixpar)
            
            self.selectallfix()
            self.updatefix()






    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
     
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
     
        return False




    def output_reduce(self, l):
        sep = [i[0] for i in zip(range(len(l)), l) if '####' in i[1]]
        name = [l[1 + i[0]].replace('\n', '') for i in zip(range(len(l)), l) if '####' in i[1]]
        name_only = set(name)
        name_only = list(name_only)
        sep_name = zip(sep, name)
        index_tot = []
        for j in name_only:
            index = [i for i in sep_name if j in i]
            index = index[-1]
            #print j, index
            index_tot.append(index)
    
        index_tot = sorted(index_tot)
        end_tot = []
        for j in xrange(len(index_tot)):
            index = [i for i in zip(sep, range(len(sep))) if i[0] == index_tot[j][0]]
            #print index, sep[-1]
            if index[0][0] != sep[-1]:
                #print index, sep[index[0][1] + 1] - 1
                end_tot.append(sep[index[0][1] + 1] - 1)
            else:
                #print index, len(l) - 1
                end_tot.append(len(l) - 1)
    
        
        output = []
        for i in xrange(len(index_tot)):
            #print index_tot[i][0], end_tot[i]
            for j in range(index_tot[i][0], end_tot[i] + 1):
                output.append(l[j])
        return output




    def set_model(self):
        #self.windows.append(Tkinter.Toplevel(self.parent))
        #self.windows[1].title("model")

        t = Tkinter.Toplevel(self.parent)
        t.title("model")
        t.geometry("1600x1100+2100+0")
        s = bwidget.ScrolledWindow(t, auto="vertical", scrollbar="vertical")
        f = bwidget.ScrollableFrame(s, constrainedwidth=True)
        g = f.getframe()
        self.windows.append(g)

        Tkinter.Button(self.windows[1], text = "All", command = self.selectallmodel).grid(row = 0, column = 0, sticky = Tkinter.W)
        Tkinter.Button(self.windows[1], text = "None", command = self.deselectallmodel).grid(row = 0, column = 1, sticky = Tkinter.W)
        #Tkinter.Button(self.windows[1], text = "Add", command = self.addmodel).grid(row = 0, column = 2, sticky = Tkinter.W)
        m = Tkinter.Menubutton(self.windows[1], text = "Add")
        m.grid(row = 0, column = 2)
        m.menu = Tkinter.Menu(m)
        m["menu"] = m.menu
        #print self.model_info
        self.addmodel_info = []
        for i in DASpec.model_name_p:
            var = Tkinter.IntVar()
            self.addmodel_info.append(var)
            m.menu.add_checkbutton(label = i, variable = var, command = self.addmodel)
        Tkinter.Button(self.windows[1], text = "Delete", command = self.delmodel).grid(row = 0, column = 3, sticky = Tkinter.W)
        Tkinter.Button(self.windows[1], text = "Use previous result", command = self.model_useresult).grid(row = 0, column = 12, sticky = Tkinter.W)


        iwin1 = 1
        for iwin in xrange(len(self.models)):
            self.model_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[1], text = str(iwin + 1),
                variable = self.model_info[iwin][0])
            self.model_info[iwin].append(c1)
            c1.grid(row = iwin1, column = 0, sticky = Tkinter.W)
            m = Tkinter.Menubutton(self.windows[1], text = self.models[iwin][0], width = 22)
            self.model_info[iwin].append(m)
            m.grid(row = iwin1, column = 1)
            m.menu = Tkinter.Menu(m)
            m["menu"] = m.menu
            self.model_info[iwin].append([])
            #print self.model_info
            for i in DASpec.model_name_p:
                var = Tkinter.IntVar()
                self.model_info[iwin][3].append(var)
                m.menu.add_checkbutton(label = i, variable = var, command = self.updatemodel)
            #print self.model_info
            col = 2
            #print self.models[iwin]
            for ipar in xrange(len(self.models[iwin]) - 3):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][col - 1]))
                col += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-2][ipar]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2 + 1]))
                col += 1
            iwin1 += 1

        g.grid_columnconfigure(1, weight=1)
        s.setwidget(f)
        s.pack(fill="both", expand=1)
        #print self.model_info

    def updatemodel(self):
        for i in xrange(len(self.model_info)):
            #print self.model_info
            for j in xrange(len(self.model_info[i][3])):
                #print self.model_info[i][-1][j].get()
                if self.model_info[i][3][j].get() == 1:
                    #print i, j
                    itar = i
                    jtar = j
                    self.model_info[i][3][j].set(0)

        #print self.models
        self.models[itar][0] = DASpec.model_name_p[jtar]
        self.update_model_individual(itar)
        self.update_par0_individual(itar)
        self.update_limit_individual(itar)

        #print self.model_info

        #for i in self.model_info:
        for i in [self.model_info[itar]]:
            i[1].grid_forget()
            i[2].grid_forget()
            for j in xrange(len(i) - 7):
                i[j + 4].grid_forget()
            for j in i[-3]:
                j.grid_forget()
            for j in i[-2]:
                j.grid_forget()
            for j in i[-1]:
                j.grid_forget()

        #iwin1 = 1 + 3 * (len(self.models) - 2)
        #for iwin in xrange(len(self.models)):
        #for iwin in [len(self.models) - 1]:

        #self.model_info = []
        #iwin1 = 1
        iwin1 = 1 + 3 * (itar - 1)
        #for iwin in xrange(len(self.models)):
        for iwin in [itar]:
            #self.model_info.append([Tkinter.IntVar()])
            self.model_info.insert(iwin, [Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[1], text = str(iwin + 1),
                variable = self.model_info[iwin][0])
            self.model_info[iwin].append(c1)
            c1.grid(row = iwin1, column = 0, sticky = Tkinter.W)
            m = Tkinter.Menubutton(self.windows[1], text = self.models[iwin][0], width = 22)
            self.model_info[iwin].append(m)
            m.grid(row = iwin1, column = 1)
            m.menu = Tkinter.Menu(m)
            m["menu"] = m.menu
            self.model_info[iwin].append([])
            #print self.model_info
            for i in DASpec.model_name_p:
                var = Tkinter.IntVar()
                self.model_info[iwin][3].append(var)
                m.menu.add_checkbutton(label = i, variable = var, command = self.updatemodel)
            #print self.model_info
            col = 2
            #print self.models[iwin]
            for ipar in xrange(len(self.models[iwin]) - 3):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][col - 1]))
                col += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-2][ipar]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2]))
                col += 1
            col -= len(self.models[iwin][-2])
            iwin1 += 1
            self.model_info[iwin].append([])
            for ipar in xrange(len(self.models[iwin][-2])):
                p = Tkinter.Entry(self.windows[1], width = 8)
                self.model_info[iwin][-1].append(p)
                p.grid(row = iwin1, column = col)
                p.insert(0, str(self.models[iwin][-1][ipar * 2 + 1]))
                col += 1
            iwin1 += 1

    def onOpen(self):
        #dlg = tkFileDialog.Open(self, initialdir = ".")
        #self.specfile = dlg.show()
        #self.specfile = "test.input"
        wave_lim1, wave_lim2 = self.plotspec()
        self.initmodel(wave_lim1, wave_lim2)
        self.set_fitwindow()
        self.set_par0()
        self.set_limit()
        self.set_model()
        self.set_fix()
        self.set_tie()
        self.set_fitwin()
        self.set_resultwin()

    def set_resultwin(self):
        t = Tkinter.Toplevel(self.parent)
        t.title("result")
        #t.geometry("400x300+1050+750")
        #t.geometry("640x400+1050+600")
        t.geometry("1280x800+2100+1200")
        s = bwidget.ScrolledWindow(t, auto="vertical", scrollbar="vertical")
        f = bwidget.ScrollableFrame(s, constrainedwidth=True)
        g = f.getframe()
        self.windows.append(g)

        text = Tkinter.Text(g)
        self.resultwin = text
        text.pack()

        g.grid_columnconfigure(1, weight=1)
        s.setwidget(f)
        s.pack(fill="both", expand=1)

    def set_fitwin(self):
        self.windows.append(Tkinter.Toplevel(self.parent))
        #self.windows[4].geometry("300x60+0+350")
        self.windows[4].geometry("600x120+0+700")
        self.windows[4].title("fit")
        #button = Tkinter.Button(master=self.windows[4], text='set fit', command=self.set_fit)
        #button.grid(row = 0, column = 0)
        button = Tkinter.Button(master=self.windows[4], text='lmfit', command=self.lmfit)
        button.grid(row = 0, column = 0)
        button = Tkinter.Button(master=self.windows[4], text='mix_fit', command=self.mixfit)
        button.grid(row = 0, column = 1)
        button = Tkinter.Button(master=self.windows[4], text='siman', command=self.siman)
        button.grid(row = 0, column = 2)
        button = Tkinter.Button(master=self.windows[4], text='next', command=self.nextspec)
        button.grid(row = 0, column = 3)
        button = Tkinter.Button(master=self.windows[4], text='nextlmfit', command=self.next_lmfit)
        button.grid(row = 1, column = 0)
        button = Tkinter.Button(master=self.windows[4], text='autolmfit', command=self.auto_lmfit)
        button.grid(row = 1, column = 1)

    def next_lmfit(self):
        self.nextspec()
        self.lmfit()

    def auto_lmfit(self):
        while self.index <= len(self.speclist):
            self.nextspec()
            print '=' * 25, self.index, 'of', len(self.speclist), self.specname
            self.lmfit()

    def nextspec(self):
        self.index += 1
        if self.index == len(self.speclist):
            print 'fitting finished!'
            sys.exit()
        self.specfile = self.speclist[self.index]

        self.specname = self.specfile

        l = open(self.specname).readlines()
        l = [i for i in l if i.replace(" ", "")[0] != '#']
        self.wave = [float(i.split()[0]) for i in l]
        self.flux = [float(i.split()[1]) for i in l]
        self.err = [float(i.split()[2]) for i in l]
        (self.wave, self.flux, self.err) = np.array((self.wave, self.flux, self.err))
        self.scale = cal_scale(self.flux)
        self.flux = self.flux / self.scale
        self.err = self.err / self.scale

        wave_lim1 = np.min(self.wave)
        wave_lim2 = np.max(self.wave)

        for i in self.figfitwindow:
            i.remove()
        self.figspec.clf()
        #fig = Figure(figsize = (10, 8), dpi = 80)
        #self.figspec = fig
        ax = self.figspec.add_subplot(111)
        #ax = self.figspec.add_axes([0.15, 0.15, 0.8, 0.8])
        ax.step(self.wave, self.flux, where = 'mid', color = 'k')

        self.figfitwindow = []
        for i in self.fitwindow:
            axvline = self.figspec.axes[0].axvspan(i[0], i[1], ymin = 0, ymax = 1, alpha = 0.3, color = 'k')
            self.figfitwindow.append(axvline)

        ax.set_xlabel("wavelength")
        ax.set_ylabel("flux")

        #self.canvas = FigureCanvasTkAgg(self.figspec, master = self.parent)
        #self.canvas.show()
        #self.canvas.get_tk_widget().pack(side = Tkinter.TOP, fill = Tkinter.BOTH, expand = 1)
        #self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.parent)
        #self.toolbar.update()
        #self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.canvas.draw()


    def set_tie(self):
        t = Tkinter.Toplevel(self.parent)
        t.title("tie")
        #t.geometry("650x300+0+750")
        t.geometry("1300x600+0+1500")
        s = bwidget.ScrolledWindow(t, auto="vertical", scrollbar="vertical")
        f = bwidget.ScrollableFrame(s, constrainedwidth=True)
        g = f.getframe()
        self.windows.append(g)

        Tkinter.Button(self.windows[3], text = "Update", command = self.updatetie).grid(row = 0, column = 0, sticky = Tkinter.W)

        Tkinter.Button(self.windows[3], text = "All", command = self.selectalltie).grid(row = 1, column = 0, sticky = Tkinter.W)
        Tkinter.Button(self.windows[3], text = "None", command = self.deselectalltie).grid(row = 1, column = 1, sticky = Tkinter.W)
        #Tkinter.Button(self.windows[3], text = "Add", command = self.addtie).grid(row = 1, column = 2, sticky = Tkinter.W)
        m = Tkinter.Menubutton(self.windows[3], text = "Add")
        m.grid(row = 1, column = 2)
        m.menu = Tkinter.Menu(m)
        m["menu"] = m.menu
        #print self.model_info
        self.addtie_info = []
        for i in DASpec.tie_name:
            var = Tkinter.IntVar()
            self.addtie_info.append(var)
            m.menu.add_checkbutton(label = i, variable = var, command = self.addtie)
        Tkinter.Button(self.windows[3], text = "Delete", command = self.deltie).grid(row = 1, column = 3, sticky = Tkinter.W)

        g.grid_columnconfigure(1, weight=1)
        s.setwidget(f)
        s.pack(fill="both", expand=1)

    def updatetie(self):
        for i in xrange(len(self.model_info)):
            for j in xrange(len(self.model_info[i][-3])):
                self.model_info[i][-3][j].configure(background = "white")
                self.model_info[i][-2][j].configure(background = "white")
                self.model_info[i][-1][j].configure(background = "white")
                self.model_info[i][-3][j].configure(foreground = "black")
                self.model_info[i][-2][j].configure(foreground = "black")
                self.model_info[i][-1][j].configure(foreground = "black")

        self.fix = []
        for i in xrange(len(self.fix_info)):
            if self.fix_info[i][0].get():
                #print [int(self.fix_info[i][1].get()), int(self.fix_info[i][2].get()), float(self.fix_info[i][3].get())]
                self.fix.append([int(self.fix_info[i][2].get()), int(self.fix_info[i][3].get()), float(self.fix_info[i][4].get())])
                self.model_info[int(self.fix_info[i][2].get()) - 1][-3][int(self.fix_info[i][3].get()) - 1].delete(0, Tkinter.END)
                self.model_info[int(self.fix_info[i][2].get()) - 1][-3][int(self.fix_info[i][3].get()) - 1].insert(0, str(float(self.fix_info[i][4].get())))
                self.model_info[int(self.fix_info[i][2].get()) - 1][-3][int(self.fix_info[i][3].get()) - 1].configure(background = "red")
                self.model_info[int(self.fix_info[i][2].get()) - 1][-2][int(self.fix_info[i][3].get()) - 1].configure(background = "red")
                self.model_info[int(self.fix_info[i][2].get()) - 1][-1][int(self.fix_info[i][3].get()) - 1].configure(background = "red")

        self.tie = []
        for i in xrange(len(self.tie_info)):
            if self.tie_info[i][0].get():
                if len(self.tie_info[i]) - 3 == 6:
                    self.tie.append([int(self.tie_info[i][3].get()), int(self.tie_info[i][4].get()), float(self.tie_info[i][5].get()),
                        int(self.tie_info[i][6].get()), int(self.tie_info[i][7].get()), float(self.tie_info[i][8].get())])
                    temp = self.model_info[int(self.tie_info[i][5].get()) - 1][-3][int(self.tie_info[i][6].get()) - 1].get()
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].delete(0, Tkinter.END)
                    if int(self.tie_info[i][7].get()) == 0:
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].insert(0, str(float(temp) * float(self.tie_info[i][8].get())))
                    elif int(self.tie_info[i][7].get()) == 1:
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].insert(0, str(float(temp) + float(self.tie_info[i][8].get())))
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-2][int(self.tie_info[i][4].get()) - 1].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-1][int(self.tie_info[i][4].get()) - 1].configure(background = "green")
                    self.model_info[int(self.tie_info[i][5].get()) - 1][-3][int(self.tie_info[i][6].get()) - 1].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][5].get()) - 1][-2][int(self.tie_info[i][6].get()) - 1].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][5].get()) - 1][-1][int(self.tie_info[i][6].get()) - 1].configure(foreground = "green")
                elif len(self.tie_info[i]) - 3 == 2:
                    self.tie.append([int(self.tie_info[i][3].get()), int(self.tie_info[i][4].get())])
                    temp = []
                    for j in xrange(len(self.model_info[int(self.tie_info[i][4].get()) - 1][-3]) - 1):
                        temp.append(self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].get())
                    for j in xrange(len(self.model_info[int(self.tie_info[i][3].get()) - 1][-3]) - 1):
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].delete(0, Tkinter.END)
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].insert(0, float(temp[j]))
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-2][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-1][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-2][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-1][j + 1].configure(foreground = "green")
                elif len(self.tie_info[i]) - 3 == 3:
                    self.tie.append([int(self.tie_info[i][3].get()), int(self.tie_info[i][4].get()), float(self.tie_info[i][5].get())])
                    temp0 = self.model_info[int(self.tie_info[i][4].get()) - 1][-3][0].get()
                    temp = []
                    for j in xrange(len(self.model_info[int(self.tie_info[i][4].get()) - 1][-3]) - 1):
                        temp.append(self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].get())
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][0].delete(0, Tkinter.END)
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][0].insert(0, float(temp0) * float(self.tie_info[i][5].get()))
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][0].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-2][0].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-1][0].configure(background = "green")
                    self.model_info[int(self.tie_info[i][4].get()) - 1][-3][0].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][4].get()) - 1][-2][0].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][4].get()) - 1][-1][0].configure(foreground = "green")
                    for j in xrange(len(self.model_info[int(self.tie_info[i][3].get()) - 1][-3]) - 1):
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].delete(0, Tkinter.END)
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].insert(0, float(temp[j]))
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-2][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-1][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-2][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-1][j + 1].configure(foreground = "green")


    def selectalltie(self):
        for i in self.tie_info:
            i[1].select()

    def deselectalltie(self):
        for i in self.tie_info:
            i[1].deselect()

    def addtie_from_known(self, tietype, tiepar):
        # for j in xrange(len(self.addtie_info)):
        #     if self.addtie_info[j].get() == 1:
        #         #print j
        #         typ = j
        #         self.addtie_info[j].set(0)

        if tietype == '':
            typ = 0
        elif tietype == 'profile':
            typ = 1
        elif tietype == 'flux_profile':
            typ = 2

        if typ == 0:
            self.tie_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[3], text = str(len(self.tie_info))
                    , variable = self.tie_info[len(self.tie_info) - 1][0])
            c1.grid(row = len(self.tie_info) + 1, column = 0, sticky = Tkinter.W)
            self.tie_info[-1].append(c1)
            l = Tkinter.Label(self.windows[3], text = "tie")
            self.tie_info[-1].append(l)
            l.grid(row = len(self.tie_info) + 1, column = 1, sticky = Tkinter.W)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 2)
            e11.insert(0, str(tiepar[0]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 3)
            e11.insert(0, str(tiepar[1]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 4)
            e11.insert(0, str(tiepar[2]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 5)
            e11.insert(0, str(tiepar[3]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 6)
            e11.insert(0, str(tiepar[4]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 7)
            e11.insert(0, str(tiepar[5]))
        elif typ == 1:
            self.tie_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[3], text = str(len(self.tie_info))
                    , variable = self.tie_info[len(self.tie_info) - 1][0])
            c1.grid(row = len(self.tie_info) + 1, column = 0, sticky = Tkinter.W)
            self.tie_info[-1].append(c1)
            l = Tkinter.Label(self.windows[3], text = "profile")
            self.tie_info[-1].append(l)
            l.grid(row = len(self.tie_info) + 1, column = 1, sticky = Tkinter.W)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 2)
            e11.insert(0, str(tiepar[0]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 3)
            e11.insert(0, str(tiepar[1]))
        elif typ == 2:
            self.tie_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[3], text = str(len(self.tie_info))
                    , variable = self.tie_info[len(self.tie_info) - 1][0])
            c1.grid(row = len(self.tie_info) + 1, column = 0, sticky = Tkinter.W)
            self.tie_info[-1].append(c1)
            l = Tkinter.Label(self.windows[3], text = "flux_profile")
            self.tie_info[-1].append(l)
            l.grid(row = len(self.tie_info) + 1, column = 1, sticky = Tkinter.W)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 2)
            e11.insert(0, str(tiepar[0]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 3)
            e11.insert(0, str(tiepar[1]))
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 4)
            e11.insert(0, str(tiepar[2]))

    def addtie(self):
        for j in xrange(len(self.addtie_info)):
            if self.addtie_info[j].get() == 1:
                #print j
                typ = j
                self.addtie_info[j].set(0)

        if typ == 0:
            self.tie_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[3], text = str(len(self.tie_info))
                    , variable = self.tie_info[len(self.tie_info) - 1][0])
            c1.grid(row = len(self.tie_info) + 1, column = 0, sticky = Tkinter.W)
            self.tie_info[-1].append(c1)
            l = Tkinter.Label(self.windows[3], text = "tie")
            self.tie_info[-1].append(l)
            l.grid(row = len(self.tie_info) + 1, column = 1, sticky = Tkinter.W)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 2)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 3)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 4)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 5)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 6)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 7)
        elif typ == 1:
            self.tie_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[3], text = str(len(self.tie_info))
                    , variable = self.tie_info[len(self.tie_info) - 1][0])
            c1.grid(row = len(self.tie_info) + 1, column = 0, sticky = Tkinter.W)
            self.tie_info[-1].append(c1)
            l = Tkinter.Label(self.windows[3], text = "profile")
            self.tie_info[-1].append(l)
            l.grid(row = len(self.tie_info) + 1, column = 1, sticky = Tkinter.W)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 2)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 3)
        elif typ == 2:
            self.tie_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[3], text = str(len(self.tie_info))
                    , variable = self.tie_info[len(self.tie_info) - 1][0])
            c1.grid(row = len(self.tie_info) + 1, column = 0, sticky = Tkinter.W)
            self.tie_info[-1].append(c1)
            l = Tkinter.Label(self.windows[3], text = "flux_profile")
            self.tie_info[-1].append(l)
            l.grid(row = len(self.tie_info) + 1, column = 1, sticky = Tkinter.W)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 2)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 3)
            e11 = Tkinter.Entry(self.windows[3], width = 8)
            self.tie_info[-1].append(e11)
            e11.grid(row = len(self.tie_info) + 1, column = 4)

        #print self.tie_info


    def deltie(self):
        if self.tie_info != []:
            for i in xrange(len(self.tie_info[-1]) - 1):
                self.tie_info[-1][i + 1].grid_forget()
            del self.tie_info[-1]
            return 1
        else:
            return 0

    def set_fix(self):
        #self.windows.append(Tkinter.Toplevel(self.parent))
        #self.windows[2].title("fix")

        t = Tkinter.Toplevel(self.parent)
        t.title("fix")
        #t.geometry("300x300+0+410")
        t.geometry("600x600+0+840")
        s = bwidget.ScrolledWindow(t, auto="vertical", scrollbar="vertical")
        f = bwidget.ScrollableFrame(s, constrainedwidth=True)
        g = f.getframe()
        self.windows.append(g)

        Tkinter.Button(self.windows[2], text = "Update", command = self.updatefix).grid(row = 0, column = 0, sticky = Tkinter.W)

        Tkinter.Button(self.windows[2], text = "All", command = self.selectallfix).grid(row = 1, column = 0, sticky = Tkinter.W)
        Tkinter.Button(self.windows[2], text = "None", command = self.deselectallfix).grid(row = 1, column = 1, sticky = Tkinter.W)
        Tkinter.Button(self.windows[2], text = "Add", command = self.addfix).grid(row = 1, column = 2, sticky = Tkinter.W)
        Tkinter.Button(self.windows[2], text = "Delete", command = self.delfix).grid(row = 1, column = 3, sticky = Tkinter.W)

        g.grid_columnconfigure(1, weight=1)
        s.setwidget(f)
        s.pack(fill="both", expand=1)

    def updatefix(self):
        for i in xrange(len(self.model_info)):
            for j in xrange(len(self.model_info[i][-3])):
                self.model_info[i][-3][j].configure(background = "white")
                self.model_info[i][-2][j].configure(background = "white")
                self.model_info[i][-1][j].configure(background = "white")
        #print self.model_info
        #print self.models
        self.fix = []
        for i in xrange(len(self.fix_info)):
            if self.fix_info[i][0].get():
                #print [int(self.fix_info[i][1].get()), int(self.fix_info[i][2].get()), float(self.fix_info[i][3].get())]
                self.fix.append([int(self.fix_info[i][2].get()), int(self.fix_info[i][3].get()), float(self.fix_info[i][4].get())])
                self.model_info[int(self.fix_info[i][2].get()) - 1][-3][int(self.fix_info[i][3].get()) - 1].delete(0, Tkinter.END)
                self.model_info[int(self.fix_info[i][2].get()) - 1][-3][int(self.fix_info[i][3].get()) - 1].insert(0, str(float(self.fix_info[i][4].get())))
                self.model_info[int(self.fix_info[i][2].get()) - 1][-3][int(self.fix_info[i][3].get()) - 1].configure(background = "red")
                self.model_info[int(self.fix_info[i][2].get()) - 1][-2][int(self.fix_info[i][3].get()) - 1].configure(background = "red")
                self.model_info[int(self.fix_info[i][2].get()) - 1][-1][int(self.fix_info[i][3].get()) - 1].configure(background = "red")
        #print self.fix

        self.tie = []
        for i in xrange(len(self.tie_info)):
            if self.tie_info[i][0].get():
                if len(self.tie_info[i]) - 3 == 6:
                    self.tie.append([int(self.tie_info[i][3].get()), int(self.tie_info[i][4].get()), float(self.tie_info[i][5].get()),
                        int(self.tie_info[i][6].get()), int(self.tie_info[i][7].get()), float(self.tie_info[i][8].get())])
                    temp = self.model_info[int(self.tie_info[i][5].get()) - 1][-3][int(self.tie_info[i][6].get()) - 1].get()
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].delete(0, Tkinter.END)
                    if int(self.tie_info[i][7].get()) == 0:
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].insert(0, str(float(temp) * float(self.tie_info[i][8].get())))
                    elif int(self.tie_info[i][7].get()) == 1:
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].insert(0, str(float(temp) + float(self.tie_info[i][8].get())))
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][int(self.tie_info[i][4].get()) - 1].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-2][int(self.tie_info[i][4].get()) - 1].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-1][int(self.tie_info[i][4].get()) - 1].configure(background = "green")
                    self.model_info[int(self.tie_info[i][5].get()) - 1][-3][int(self.tie_info[i][6].get()) - 1].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][5].get()) - 1][-2][int(self.tie_info[i][6].get()) - 1].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][5].get()) - 1][-1][int(self.tie_info[i][6].get()) - 1].configure(foreground = "green")
                elif len(self.tie_info[i]) - 3 == 2:
                    self.tie.append([int(self.tie_info[i][3].get()), int(self.tie_info[i][4].get())])
                    temp = []
                    for j in xrange(len(self.model_info[int(self.tie_info[i][4].get()) - 1][-3]) - 1):
                        temp.append(self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].get())
                    for j in xrange(len(self.model_info[int(self.tie_info[i][3].get()) - 1][-3]) - 1):
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].delete(0, Tkinter.END)
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].insert(0, float(temp[j]))
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-2][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-1][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-2][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-1][j + 1].configure(foreground = "green")
                elif len(self.tie_info[i]) - 3 == 3:
                    self.tie.append([int(self.tie_info[i][3].get()), int(self.tie_info[i][4].get()), float(self.tie_info[i][5].get())])
                    temp0 = self.model_info[int(self.tie_info[i][4].get()) - 1][-3][0].get()
                    temp = []
                    for j in xrange(len(self.model_info[int(self.tie_info[i][4].get()) - 1][-3]) - 1):
                        temp.append(self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].get())
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][0].delete(0, Tkinter.END)
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][0].insert(0, float(temp0) * float(self.tie_info[i][5].get()))
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-3][0].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-2][0].configure(background = "green")
                    self.model_info[int(self.tie_info[i][3].get()) - 1][-1][0].configure(background = "green")
                    self.model_info[int(self.tie_info[i][4].get()) - 1][-3][0].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][4].get()) - 1][-2][0].configure(foreground = "green")
                    self.model_info[int(self.tie_info[i][4].get()) - 1][-1][0].configure(foreground = "green")
                    for j in xrange(len(self.model_info[int(self.tie_info[i][3].get()) - 1][-3]) - 1):
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].delete(0, Tkinter.END)
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].insert(0, float(temp[j]))
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-3][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-2][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][3].get()) - 1][-1][j + 1].configure(background = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-3][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-2][j + 1].configure(foreground = "green")
                        self.model_info[int(self.tie_info[i][4].get()) - 1][-1][j + 1].configure(foreground = "green")



    def selectallfix(self):
        for i in self.fix_info:
            i[1].select()

    def deselectallfix(self):
        for i in self.fix_info:
            i[1].deselect()

    def addfix(self):
        self.fix_info.append([Tkinter.IntVar()])
        c1 = Tkinter.Checkbutton(self.windows[2], text = str(len(self.fix_info))
                , variable = self.fix_info[len(self.fix_info) - 1][0])
        c1.grid(row = len(self.fix_info) + 1, column = 0, sticky = Tkinter.W)
        self.fix_info[-1].append(c1)
        e11 = Tkinter.Entry(self.windows[2], width = 8)
        self.fix_info[-1].append(e11)
        e11.grid(row = len(self.fix_info) + 1, column = 1)
        e11 = Tkinter.Entry(self.windows[2], width = 8)
        self.fix_info[-1].append(e11)
        e11.grid(row = len(self.fix_info) + 1, column = 2)
        e11 = Tkinter.Entry(self.windows[2], width = 8)
        self.fix_info[-1].append(e11)
        e11.grid(row = len(self.fix_info) + 1, column = 3)

        #print self.fix_info

    def addfix_from_known(self, fixpar):
        self.fix_info.append([Tkinter.IntVar()])
        c1 = Tkinter.Checkbutton(self.windows[2], text = str(len(self.fix_info))
                , variable = self.fix_info[len(self.fix_info) - 1][0])
        c1.grid(row = len(self.fix_info) + 1, column = 0, sticky = Tkinter.W)
        self.fix_info[-1].append(c1)
        e11 = Tkinter.Entry(self.windows[2], width = 8)
        self.fix_info[-1].append(e11)
        e11.grid(row = len(self.fix_info) + 1, column = 1)
        e11.insert(0, fixpar[0])
        e11 = Tkinter.Entry(self.windows[2], width = 8)
        self.fix_info[-1].append(e11)
        e11.grid(row = len(self.fix_info) + 1, column = 2)
        e11.insert(0, fixpar[1])
        e11 = Tkinter.Entry(self.windows[2], width = 8)
        self.fix_info[-1].append(e11)
        e11.grid(row = len(self.fix_info) + 1, column = 3)
        e11.insert(0, fixpar[2])

        #print self.fix_info

    def delfix(self):
        if self.fix_info != []:
            self.fix_info[-1][1].grid_forget()
            self.fix_info[-1][2].grid_forget()
            self.fix_info[-1][3].grid_forget()
            self.fix_info[-1][4].grid_forget()
            del self.fix_info[-1]
            return 1
        else:
            return 0

    def set_fitwindow(self):
        #self.windows.append(Tkinter.Toplevel(self.parent))
        #self.windows[0].title("fit window")

        t = Tkinter.Toplevel(self.parent)
        t.title("fit windows")
        #t.geometry("300x300+0+0")
        t.geometry("600x600+0+0")
        s = bwidget.ScrolledWindow(t, auto="vertical", scrollbar="vertical")
        f = bwidget.ScrollableFrame(s, constrainedwidth=True)
        g = f.getframe()
        self.windows.append(g)

        Tkinter.Button(self.windows[0], text = "Update", command = self.updatewin).grid(row = 0, column = 0, sticky = Tkinter.W)
        Tkinter.Button(self.windows[0], text = "All", command = self.selectallwin).grid(row = 1, column = 0, sticky = Tkinter.W)
        Tkinter.Button(self.windows[0], text = "None", command = self.deselectallwin).grid(row = 1, column = 1, sticky = Tkinter.W)
        Tkinter.Button(self.windows[0], text = "Add", command = self.addwin).grid(row = 1, column = 2, sticky = Tkinter.W)
        Tkinter.Button(self.windows[0], text = "Delete", command = self.delwin).grid(row = 1, column = 3, sticky = Tkinter.W)

        for iwin in xrange(len(DASpec.fitwindows)):
            self.fitwindow_info.append([Tkinter.IntVar()])
            c1 = Tkinter.Checkbutton(self.windows[0], text = str(iwin + 1)
                , variable = self.fitwindow_info[iwin][0])
            self.fitwindow_info[iwin].append(c1)
            c1.grid(row = iwin + 2, column = 0, sticky = Tkinter.W)
            e11 = Tkinter.Entry(self.windows[0], width = 8)
            self.fitwindow_info[iwin].append(e11)
            e11.insert(0, str(DASpec.fitwindows[iwin][0]))
            e11.grid(row = iwin + 2, column = 1)
            l = Tkinter.Label(self.windows[0], text = "-")
            self.fitwindow_info[iwin].append(l)
            l.grid(row = iwin + 2, column = 2)
            e12 = Tkinter.Entry(self.windows[0], width = 8)
            self.fitwindow_info[iwin].append(e12)
            e12.insert(0, str(DASpec.fitwindows[iwin][1]))
            e12.grid(row = iwin + 2, column = 3)
        #print self.fitwindow_info
        g.grid_columnconfigure(1, weight=1)
        s.setwidget(f)
        s.pack(fill="both", expand=1)

    def updatewin(self):
        self.fitwindow = []
        #if len(self.figfitwindow) > 0:
        for i in self.figfitwindow:
            i.remove()
        self.figfitwindow = []
        for i in self.fitwindow_info:
            if i[0].get():
                self.fitwindow.append([float(i[2].get()), float(i[4].get())])
        for i in self.fitwindow:
            axvline = self.figspec.axes[0].axvspan(i[0], i[1], ymin = 0, ymax = 1, alpha = 0.3, color = 'k')
            self.figfitwindow.append(axvline)

        self.figspec.axes[0].relim()
        self.figspec.axes[0].autoscale_view()
        self.canvas.draw()

    def selectallwin(self):
        for i in self.fitwindow_info:
            i[1].select()

    def addwin(self):
        iwin = len(self.fitwindow_info)
        self.fitwindow_info.append([Tkinter.IntVar()])
        c1 = Tkinter.Checkbutton(self.windows[0], text = str(iwin + 1), variable = self.fitwindow_info[iwin][0])
        self.fitwindow_info[iwin].append(c1)
        c1.grid(row = iwin + 2, column = 0, sticky = Tkinter.W)
        e11 = Tkinter.Entry(self.windows[0], width = 8)
        self.fitwindow_info[iwin].append(e11)
        e11.grid(row = iwin + 2, column = 1)
        l = Tkinter.Label(self.windows[0], text = "-")
        self.fitwindow_info[iwin].append(l)
        l.grid(row = iwin + 2, column = 2)
        e12 = Tkinter.Entry(self.windows[0], width = 8)
        self.fitwindow_info[iwin].append(e12)
        e12.grid(row = iwin+ 2, column = 3)

    def addwin_from_known(self, win1, win2):
        iwin = len(self.fitwindow_info)
        self.fitwindow_info.append([Tkinter.IntVar()])
        c1 = Tkinter.Checkbutton(self.windows[0], text = str(iwin + 1), variable = self.fitwindow_info[iwin][0])
        c1.select()
        self.fitwindow_info[iwin].append(c1)
        c1.grid(row = iwin + 2, column = 0, sticky = Tkinter.W)
        e11 = Tkinter.Entry(self.windows[0], width = 8)
        self.fitwindow_info[iwin].append(e11)
        e11.grid(row = iwin + 2, column = 1)
        e11.insert(0, win1)
        l = Tkinter.Label(self.windows[0], text = "-")
        self.fitwindow_info[iwin].append(l)
        l.grid(row = iwin + 2, column = 2)
        e12 = Tkinter.Entry(self.windows[0], width = 8)
        self.fitwindow_info[iwin].append(e12)
        e12.grid(row = iwin+ 2, column = 3)
        e12.insert(0, win2)

    def delwin(self):
        self.fitwindow_info[-1][1].grid_forget()
        self.fitwindow_info[-1][2].grid_forget()
        self.fitwindow_info[-1][3].grid_forget()
        self.fitwindow_info[-1][4].grid_forget()
        del self.fitwindow_info[-1]
        #print self.fitwindow_info

    def deselectallwin(self):
        for i in self.fitwindow_info:
            i[1].deselect()

    def plotspec_after_fit(self):
        for i in self.figfitwindow:
            i.remove()
        self.figspec.clf()
        ax = self.figspec.add_axes([0.15, 0.35, 0.8, 0.6])
        ax.step(self.wave, self.flux, where = 'mid', color = 'k')
        #ax.set_xlabel("wavelength")
        ax.set_ylabel("flux")

        #print 'test7'
        ax.plot(self.wave, self.curvefit.calc(self.wave))
        nmodel = 0
        for i in xrange(len(self.model_info)):
            if self.model_info[i][0].get():
                nmodel += 1
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'purple']
        #print 'test8'
        #print nmodel

        co = 0
        for i in xrange(nmodel):
            if co >= len(colors):
                co -= len(colors)
            #print 'i', i
            self.curvefit.calc_comp(i + 1, self.wave)
            ax.plot(self.wave, self.curvefit.calc_comp(i + 1, self.wave), color = colors[co])
            co += 1
        #print 'test9'

        self.figfitwindow = []
        for i in self.fitwindow:
            axvline = self.figspec.axes[0].axvspan(i[0], i[1], ymin = 0, ymax = 1, alpha = 0.3, color = 'k')
            self.figfitwindow.append(axvline)

        [i.set_visible(False) for i in ax.get_xticklabels()]

        ax = self.figspec.add_axes([0.15, 0.14, 0.8, 0.2], sharex = ax)
        ax.step(self.wave, self.flux - self.curvefit.calc(self.wave), where = 'mid', color = 'k')
        ax.axhline(0.0, linestyle = '--', color = '0.3')
        ax.set_xlabel("wavelength")
        ax.set_ylabel("resi")

        for i in self.fitwindow:
            axvline = self.figspec.axes[1].axvspan(i[0], i[1], ymin = 0, ymax = 1, alpha = 0.3, color = 'k')
            self.figfitwindow.append(axvline)

        self.figspec.axes[0].relim()
        self.figspec.axes[0].autoscale_view()
        self.figspec.axes[1].relim()
        self.figspec.axes[1].autoscale_view()
        self.canvas.draw()

    def plotspec(self):
        #dlg = tkFileDialog.Open(self, initialdir = ".")
        #fl = dlg.show()
        fl = self.specfile
        #fl = "test.input"

        if fl != '':
            self.specname = fl

            l = open(self.specname).readlines()
            l = [i for i in l if i.replace(" ", "")[0] != '#']
            self.wave = [float(i.split()[0]) for i in l]
            self.flux = [float(i.split()[1]) for i in l]
            self.err = [float(i.split()[2]) for i in l]
            (self.wave, self.flux, self.err) = np.array((self.wave, self.flux, self.err))
            self.scale = cal_scale(self.flux)
            self.flux = self.flux / self.scale
            self.err = self.err / self.scale

            wave_lim1 = np.min(self.wave)
            wave_lim2 = np.max(self.wave)
            #self.windows = []
            #for i in DASpec.fitwindows:
            #    if not ((i[0] > wave_lim2) or (i[1] < wave_lim1)):
            #        self.windows.append(i)
            
            mpl.rcParams['font.size'] = 24.0
            fig = Figure(figsize = (8, 6), dpi = 80)
            self.figspec = fig
            ax = fig.add_subplot(111)
            #for i in self.windows:
            #    ax.axvspan(i[0], i[1], ymin = 0, ymax = 1, alpha = 0.3, color = 'k')
            ax.step(self.wave, self.flux, where = 'mid', color = 'k')

            ax.set_xlabel("wavelength")
            ax.set_ylabel("flux")

            self.canvas = FigureCanvasTkAgg(fig, master = self.parent)
            #self.canvas.show()
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side = Tkinter.TOP, fill = Tkinter.BOTH, expand = 1)
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.parent)
            self.toolbar.update()
            self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)

            return wave_lim1, wave_lim2

            #self.initmodel(wave_lim1, wave_lim2)

    def lmfit(self):
        self.set_fit()
        #print 'test4'
        #self.curvefit.info()
        self.curvefit.lmfit()
        #self.curvefit.info()
        #print 'test5'

        par_tot = self.curvefit.par_tot()
        output_par = "par "
        for i in par_tot:
            output_par += '%e ' % i
        output_par += "\n"
        parerr_tot = self.curvefit.parerr_tot()
        output_parerr = "par_error "
        for i in parerr_tot:
            output_parerr += '%e ' % i
        output_parerr += "\n"
        #self.resultwin.insert(Tkinter.END, self.specfile + '\n')
        self.resultwin.insert(Tkinter.END, '# reduced chisq: %f\n' % self.curvefit.reduced_chisq())
        self.resultwin.insert(Tkinter.END, '# result\n')
        #self.resultwin.insert(Tkinter.END, output_par)
        #self.resultwin.insert(Tkinter.END, output_parerr)
        #print 'test6'
        npar = []
        for i in xrange(len(self.curvefit.model.comps)):
            npar.append(self.curvefit.model.comps[i].func.npar)

        u = 0
        for i in xrange(len(npar)):
            text = 'par of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%.3e ' % (par_tot[u])
                u += 1
            text += '\n'
            self.resultwin.insert(Tkinter.END, text)
        u = 0
        for i in xrange(len(npar)):
            text = 'err of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%.3e ' % (parerr_tot[u])
                u += 1
            text += '\n'
            self.resultwin.insert(Tkinter.END, text)

        #self.outputfile.write(self.specfile + '\n')
        self.outputfile.write('# reduced chisq: %f\n' % self.curvefit.reduced_chisq())
        self.outputfile.write('# result:\n')
        #self.outputfile.write(output_par)
        #self.outputfile.write(output_parerr)
        u = 0
        for i in xrange(len(npar)):
            text = 'par of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%e ' % (par_tot[u])
                u += 1
            text += '\n'
            self.outputfile.write(text)
        u = 0
        for i in xrange(len(npar)):
            text = 'err of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%e ' % (parerr_tot[u])
                u += 1
            text += '\n'
            self.outputfile.write(text)

        self.outputfile.flush()

        self.plotspec_after_fit()


    def mixfit(self):
        self.set_fit()
        self.curvefit.mix_fit()
        #print self.curvefit.par()
        par_tot = self.curvefit.par_tot()
        output_par = "par "
        for i in par_tot:
            output_par += '%e ' % i
        output_par += "\n"
        parerr_tot = self.curvefit.parerr_tot()
        output_parerr = "par_error "
        for i in parerr_tot:
            output_parerr += '%e ' % i
        output_parerr += "\n"
        #self.resultwin.insert(Tkinter.END, self.specfile + '\n')
        #self.resultwin.insert(Tkinter.END, output_par)
        #self.resultwin.insert(Tkinter.END, output_parerr)
        self.resultwin.insert(Tkinter.END, '# reduced chisq: %f\n' % self.curvefit.reduced_chisq())
        self.resultwin.insert(Tkinter.END, '# result\n')

        npar = []
        for i in xrange(len(self.curvefit.model.comps)):
            npar.append(self.curvefit.model.comps[i].func.npar)

        u = 0
        for i in xrange(len(npar)):
            text = 'par of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%.3e ' % (par_tot[u])
                u += 1
            text += '\n'
            self.resultwin.insert(Tkinter.END, text)
        u = 0
        for i in xrange(len(npar)):
            text = 'err of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%.3e ' % (parerr_tot[u])
                u += 1
            text += '\n'
            self.resultwin.insert(Tkinter.END, text)

        #self.outputfile.write(self.specfile + '\n')
        #self.outputfile.write(output_par)
        #self.outputfile.write(output_parerr)
        self.outputfile.write('# reduced chisq: %f\n' % self.curvefit.reduced_chisq())
        self.outputfile.write('# result:\n')
        u = 0
        for i in xrange(len(npar)):
            text = 'par of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%e ' % (par_tot[u])
                u += 1
            text += '\n'
            self.outputfile.write(text)
        u = 0
        for i in xrange(len(npar)):
            text = 'err of comp %i: ' % (i + 1)
            for j in xrange(npar[i]):
                text += '%e ' % (parerr_tot[u])
                u += 1
            text += '\n'
            self.outputfile.write(text)


        self.outputfile.flush()

        self.plotspec_after_fit()

    def siman(self):
        self.set_fit()
        self.curvefit.siman()
        #print self.curvefit.par()
        par_tot = self.curvefit.par_tot()
        output_par = "par "
        for i in par_tot:
            output_par += '%e ' % i
        output_par += "\n"
        parerr_tot = self.curvefit.parerr_tot()
        output_parerr = "par_error "
        for i in parerr_tot:
            output_parerr += '%e ' % i
        output_parerr += "\n"
        #self.resultwin.insert(Tkinter.END, self.specfile + '\n')
        self.resultwin.insert(Tkinter.END, output_par)
        self.resultwin.insert(Tkinter.END, output_parerr)

        #self.outputfile.write(self.specfile + '\n')
        self.outputfile.write(output_par)
        self.outputfile.write(output_parerr)
        self.outputfile.flush()

        self.plotspec_after_fit()

    def find_comp(self, index):
        index0 = np.arange(index)
        n = 0
        for i in index0:
            if self.model_info[i][0].get():
                n += 1
        return n# - 1

    def set_fit(self):

        fitwindows = []
        for i in self.fitwindow_info:
            if i[0].get():
                fitwindows.append([float(i[2].get()), float(i[4].get())])
        #print fitwindows

        self.resultwin.insert(Tkinter.END, '#' * 20 + ' ' + str(self.index + 1) + ' \n')
        self.outputfile.write('#' * 20 + ' ' + str(self.index + 1) + ' \n')
        self.resultwin.insert(Tkinter.END, self.specfile + '\n')
        self.outputfile.write(self.specfile + '\n')
        self.resultwin.insert(Tkinter.END, '# unit:\n')
        self.resultwin.insert(Tkinter.END, '%e\n' % (self.scale))
        self.outputfile.write('# unit:\n')
        self.outputfile.write('%e\n' % (self.scale))
        self.resultwin.insert(Tkinter.END, '# window:\n')
        self.outputfile.write('# window:\n')

        for i in fitwindows:
            text = '[%.2f %.2f] ' % (i[0], i[1])
            self.resultwin.insert(Tkinter.END, text)
            text1 = '[%.3f %.3f] ' % (i[0], i[1])
            self.outputfile.write(text1)
        self.resultwin.insert(Tkinter.END, '\n')
        self.outputfile.write('\n')

        self.wave_fit = np.array([])
        self.flux_fit = np.array([])
        self.err_fit = np.array([])

        for i in fitwindows:
            #print i[0], i[1]
            index = np.where((self.wave >= i[0]) & (self.wave <= i[1]))
            #print index
            self.wave_fit = np.append(self.wave_fit, self.wave[index[0]])
            self.flux_fit = np.append(self.flux_fit, self.flux[index[0]])
            self.err_fit = np.append(self.err_fit, self.err[index[0]])
        #print self.wave_fit

        self.model = DASpec.compcontainer()
        #par0 = []
        #print self.model_info
        model_output = []
        for i in xrange(len(self.model_info)):
            if self.model_info[i][0].get():
                if self.models[i][0] in ["template_spec_gaussian", "template_spec_dgaussian", "template_spec_lorentzian"\
                    , "template_spec_gh4", "template_spec_reddened_gaussian", "template_spec_reddened_dgaussian", \
                    "template_spec_reddened_gh4", "template_spec_reddened_lorentzian"]:

                    name_temp, profile_temp = self.template_name_profile(self.models[i][0])

                    text = "self.model.add(DASpec.%s(  " % (name_temp)
                    for j in xrange(len(self.model_info[i]) - 7):
                        if j == 1:
                            text += "'%s'," % (profile_temp)

                        if is_number(self.model_info[i][j + 4].get()):
                            text += "%s," % (str(self.model_info[i][j + 4].get()))
                        else:
                            text += "'%s'," % (str(self.model_info[i][j + 4].get()))
                    text = text[0:-1] + " ))"
                    #print text
                    eval(text)
                    model_output.append(text.split('DASpec.')[-1].replace(' ', '')[0:-1])

                else:
                    text = "self.model.add(DASpec.%s(  " % (self.models[i][0])
                    for j in xrange(len(self.model_info[i]) - 7):
                        #print self.model_info[i][j + 4].get(), self.model_info[i][j + 4].get().isdigit()
                        if is_number(self.model_info[i][j + 4].get()):
                            text += "%s," % (str(self.model_info[i][j + 4].get()))
                        else:
                            text += "'%s'," % (str(self.model_info[i][j + 4].get()))
                    text = text[0:-1] + " ))"
                    #print text
                    eval(text)
                    model_output.append(text.split('DASpec.')[-1].replace(' ', '')[0:-1])
        #model.info()
        #print model_output

        self.resultwin.insert(Tkinter.END, '# model:\n')
        self.outputfile.write('# model:\n')
        ilabel = 1
        for iprint in model_output:
            self.resultwin.insert(Tkinter.END, str(ilabel) + ' ')
            self.outputfile.write(str(ilabel) + ' ')
            self.resultwin.insert(Tkinter.END, iprint + '\n')
            self.outputfile.write(iprint + '\n')
            ilabel += 1

        fix_output = []
        #print self.fix_info
        for i in xrange(len(self.fix_info)):
            if self.fix_info[i][0].get():
                #self.model.addfix(int(self.fix_info[i][2].get()), int(self.fix_info[i][3].get()), float(self.fix_info[i][4].get()))
                self.model.addfix(self.find_comp(int(self.fix_info[i][2].get())), int(self.fix_info[i][3].get()), float(self.fix_info[i][4].get()))
                fix_output.append('comp:%i par:%i value:%.3e' % (int(self.fix_info[i][2].get()), int(self.fix_info[i][3].get()), float(self.fix_info[i][4].get())))
        #print fix_output

        self.resultwin.insert(Tkinter.END, '# fix:\n')
        self.outputfile.write('# fix:\n')
        ilabel = 1
        for iprint in fix_output:
            self.resultwin.insert(Tkinter.END, str(ilabel) + ' ')
            self.outputfile.write(str(ilabel) + ' ')
            self.resultwin.insert(Tkinter.END, iprint + '\n')
            self.outputfile.write(iprint + '\n')
            ilabel += 1

        #print self.tie_info
        #print self.tie
        #for i in xrange(len(self.tie_info)):
            #if self.tie_info[i][0].get():
                #print self.tie_info[i][2].get()
        tie_output = []
        for i in xrange(len(self.tie)):
            if len(self.tie[i]) == 6:
                if self.tie[i][4] == 0:
                    temp_type = 'ratio'
                elif self.tie[i][4] == 1:
                    temp_type = 'offset'
                self.model.addtie(self.find_comp(int(self.tie[i][0])), int(self.tie[i][1]),
                    self.find_comp(int(self.tie[i][2])), int(self.tie[i][3]),
                    temp_type, float(self.tie[i][5]))
                    #int(self.tie[i][4]), float(self.tie[i][5]))
                tie_output.append('comp:%i par:%i -> comp:%i par:%i type:%s value:%e' % \
                        (self.find_comp(int(self.tie[i][0])), int(self.tie[i][1]), 
                            self.find_comp(int(self.tie[i][2])), int(self.tie[i][3]),
                            temp_type, float(self.tie[i][5])))
            elif len(self.tie[i]) == 2:
                self.model.addtie_profile(self.find_comp(int(self.tie[i][0])), self.find_comp(int(self.tie[i][1])))
                tie_output.append('profile comp:%i -> comp:%i' % \
                        (self.find_comp(int(self.tie[i][0])), self.find_comp(int(self.tie[i][1]))))
            elif len(self.tie[i]) == 3:
                #print int(self.tie[i][0]), int(self.tie[i][1]), float(self.tie[i][2])
                #print self.find_comp(int(self.tie[i][0])), self.find_comp(int(self.tie[i][1]))
                self.model.addtie_flux_profile(self.find_comp(int(self.tie[i][0])), self.find_comp(int(self.tie[i][1])),
                    float(self.tie[i][2]))
                #print 'test1'
                tie_output.append('flux_profile comp:%i -> comp:%i value:%e' % \
                    (self.find_comp(int(self.tie[i][0])), self.find_comp(int(self.tie[i][1])),
                    float(self.tie[i][2])))

        self.resultwin.insert(Tkinter.END, '# tie:\n')
        self.outputfile.write('# tie:\n')
        ilabel = 1
        for iprint in tie_output:
            self.resultwin.insert(Tkinter.END, str(ilabel) + ' ')
            self.outputfile.write(str(ilabel) + ' ')
            self.resultwin.insert(Tkinter.END, iprint + '\n')
            self.outputfile.write(iprint + '\n')
            ilabel += 1

        #print 'test2'
        self.model.info()

        par0 = []
        lim1 = []
        lim2 = []
        for i in xrange(len(self.model_info)):
            if self.model_info[i][0].get():
                for j in xrange(len(self.model_info[i][-3])):
                    par0.append(float(self.model_info[i][-3][j].get()))
                    lim1.append(float(self.model_info[i][-2][j].get()))
                    lim2.append(float(self.model_info[i][-1][j].get()))
        #print par0
        par0 = np.array(par0)
        lim1 = np.array(lim1)
        lim2 = np.array(lim2)

        #self.model = model
        self.curvefit = DASpec.curvefit()
        self.curvefit.set_model(self.model)
        self.curvefit.set_data(self.wave_fit, self.flux_fit, self.err_fit)
        self.curvefit.set_init(self.model.parl2s(par0))

        #print lim1
        #print lim2

        lim10 = self.model.parl2s(lim1)
        lim20 = self.model.parl2s(lim2)

        #print lim10
        #print lim20

        for i in xrange(len(lim10)):
            #print i, lim10[i], 0, lim20[i], 1
            self.curvefit.set_limit(i + 1, lim10[i], 0)
            self.curvefit.set_limit(i + 1, lim20[i], 1)

        #self.curvefit = fit
        #print 'test3'


    def run(self):
        self.parent.mainloop()

    def template_name_profile(self, template_string):
        s = template_string.split('_')
        p = s[-1]
        s = s[0:-1]
        name = ''
        for i in s:
            name += i + '_'
        name = name[0:-1]
        profile = p
        return name, profile


if __name__ == "__main__":
    #root = Tkinter.Tk()
    #root.geometry("640x480+300+300")
    #app = GUI(root)
    #root.mainloop()
    a = GUI()
    a.run()
