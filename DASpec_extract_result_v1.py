#!/usr/bin/env python2

import sys
import numpy as np
import DASpec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class DASpec_result:

    def __init__(self, filename):
        self.filename = filename
        self.info_txt = open(self.filename).readlines()

        self.names = []
        self.units = []
        self.windows = []
        self.models = []
        self.DAmodels = []
        self.fixes = []
        self.ties = []
        self.chisqs = []
        self.pars = []
        self.errs = []
        self.pararrays = []
        self.errarrays = []

        sep = [i[0] for i in zip(range(len(self.info_txt)), self.info_txt) if '####' in i[1]]

        self.num = len(sep)

        l = self.info_txt
        for i in xrange(self.num):
            name = l[sep[i] + 1].split('\n')[0]
            self.names.append(name)

            x = sep[i] + 1
            while 1:
                if l[x][0] == '#' and l[x].split()[1] == 'unit:':
                    unit = float(l[x + 1].split('\n')[0])
                    break
                else:
                    x += 1
            self.units.append(unit)

            x = sep[i] + 1
            while 1:
                if l[x][0] == '#' and l[x].split()[1] == 'window:':
                    window = [[float(k) for k in j.split(']')[0].split()] for j in l[x + 1].replace('\n', '').split('[')[1:]]
                    break
                else:
                    x += 1
            self.windows.append(window)

            self.models.append([])
            x = sep[i] + 1
            while 1:
                if l[x][0] == '#' and l[x].split()[1] == 'model:':
                    break
                else:
                    x += 1
            y = x + 1
            while 1:
                if x == len(l):
                    break
                if l[x][0:5] == '# fix':
                    break
                else:
                    x += 1
            z = x + 0
            for j in l[y: z]:
                self.models[-1].append(j.split()[1])

            self.fixes.append([])
            x = sep[i] + 1
            while 1:
                if l[x][0] == '#' and l[x].split()[1] == 'fix:':
                    break
                else:
                    x += 1
            y = x + 1
            while 1:
                if x == len(l):
                    break
                if l[x][0:5] == '# tie':
                    break
                else:
                    x += 1
            z = x + 0
            for j in l[y: z]:
                self.fixes[-1].append([eval(k.split(':')[1]) for k in j.split()[1:]])

            self.ties.append([])
            x = sep[i] + 1
            while 1:
                if l[x][0] == '#' and l[x].split()[1] == 'tie:':
                    break
                else:
                    x += 1
            y = x + 1
            while 1:
                if x == len(l):
                    break
                if l[x][0:5] == '# red':
                    break
                else:
                    x += 1
            z = x + 0
            for j in l[y: z]:
                if len(j.split()) == 8:
                    self.ties[-1].append([eval(k.split(':')[1]) for k in j.replace('->', '').replace('ratio', '0').replace('offset', '1').split()[1:]])
                elif len(j.split()) == 6:
                    self.ties[-1].append([j.split()[1]] + [eval(k.split(':')[1]) for k in j.replace('->', '').split()[2:]])
                elif len(j.split()) == 5:
                    self.ties[-1].append([j.split()[1]] + [eval(k.split(':')[1]) for k in j.replace('->', '').split()[2:]])

            x = sep[i] + 1
            while 1:
                if l[x][0] == '#' and l[x].split()[1] == 'reduced':
                    chisq = float(l[x].split()[-1])
                    break
                else:
                    x += 1
            self.chisqs.append(chisq)

            x = sep[i] + 1
            while 1:
                if l[x][0] == '#' and l[x].split()[1] == 'result:':
                    break
                else:
                    x += 1
            y = x + 1
            while 1:
                if x == len(l):
                    break
                if l[x][0] == '#' and l[x][1] == '#':
                    break
                else:
                    x += 1
            z = x + 0
            par_err_i = l[y: z]
            num = len(par_err_i) / 2
            par_i = par_err_i[0: num]
            err_i = par_err_i[num: 2 * num]
            #print par_i

            par_i = [[float(k) for k in j.split(':')[1].split('\n')[0].split()] for j in par_i]
            err_i = [[float(k) for k in j.split(':')[1].split('\n')[0].split()] for j in err_i]

            self.pars.append(par_i)
            self.errs.append(err_i)

            par_ii = []
            err_ii = []
            for j in par_i:
                par_ii += j
            for j in err_i:
                err_ii += j
            self.pararrays.append(par_ii)
            self.errarrays.append(err_ii)

        for i in range(len(self.models)):
            self.DAmodels.append(DASpec.compcontainer())
            for j in range(len(self.models[i])):
                eval("self.DAmodels[i].add(DASpec." + self.models[i][j] + ")")

        self.names = np.array(self.names)
        self.units = np.array(self.units)
        self.windows = np.array(self.windows)
        self.models = np.array(self.models)
        self.fixes = np.array(self.fixes)
        self.ties = np.array(self.ties)
        self.chisqs = np.array(self.chisqs)
        self.pars = np.array(self.pars)
        self.errs = np.array(self.errs)
        self.pararrays = np.array(self.pararrays)
        self.errarrays = np.array(self.errarrays)

    def separate_ties_group(self, ties):
        a = [[]]
        for i in range(len(ties)):
            if i == 0:
                a[0].append(ties[i][1])
                a[0].append(ties[i][2])
            else:
                for j in range(len(a)):
                    label = -1
                    if ties[i][1] in a[j] or ties[i][2] in a[j]:
                        label = j
                    if label != -1:
                        a[label].append(ties[i][1])
                        a[label].append(ties[i][2])
                    else:
                        a.append([])
                        a[-1].append(ties[i][1])
                        a[-1].append(ties[i][2])

        b = []
        for i in range(len(a)):
            # print list(set(a[i]))
            b.append(np.sort(list(set(a[i]))))

        return b


    def plot_fitting_result(self, continuum_base = 1):

        pdf = PdfPages("fitting_results.pdf")

        # colors_for_tie = ['b', 'g', 'r', 'c', 'm', 'y', 'lightcoral', 'brown', 'olive', 'crimson', 'pink', 'lightpink', 'teal', 'limegreen', 'aquamarine']

        for i in range(len(self.names)):
            color_groups = self.separate_ties_group(self.ties[i])

            l = open(self.names[i]).readlines()
            w = [float(j.split()[0]) for j in l]
            f = [float(j.split()[1]) for j in l]
            (w, f) = np.array((w, f))
            f = f / self.units[i]

            winmin = self.windows[i][0][0]
            winmax = self.windows[i][0][1]

            for j in range(len(self.windows[i])):
                if winmin > self.windows[i][j][0]:
                    winmin = self.windows[i][j][0]
                if winmax < self.windows[i][j][1]:
                    winmax = self.windows[i][j][1]
            
            # print winmin, winmax

            dwin = winmax - winmin

            index = np.where((w >= winmin - 0.1 * dwin) & (w <= winmax + 0.1 * dwin))
            w1 = w[index[0]]
            f1 = f[index[0]]
            fmin = np.min(f[index[0]])
            fmax = np.max(f[index[0]])
            df = fmax - fmin

            fig = plt.figure()
            ax = fig.add_subplot(111)

            for j in range(len(self.windows[i])):
                plt.axvspan(self.windows[i][j][0], self.windows[i][j][1], alpha = 0.1, color = "0.1")

            ax.plot(w, f, color = "k")
            ax.set_xlim(winmin - 0.1 * dwin, winmax + 0.1 * dwin)
            ax.set_ylim(fmin - 0.1 * df, fmax + 0.1 * df)
            plt.title(self.names[i])
            plt.xlabel(r"$\mathrm{Wavelength\ (\AA)}$")
            plt.ylabel(r"$\mathrm{Flux\ (\times 10^{%i}\ erg\ s^{-1}\ cm^{-2}\ \AA^{-1})}$" % (np.log10(self.units[i])))

            lines = []
            plt.plot(w, self.DAmodels[i].calc(w, self.pararrays[i]))
            for j in range(len(self.pars[i])):
                
                if j + 1 == continuum_base:
                    label = 0
                    for k in range(len(color_groups)):
                        if j + 1 in color_groups[k][1:]:
                            label += 1
                            lines.append(plt.plot(w, self.DAmodels[i].calc_comp(j + 1, w, self.pararrays[i]), color = lines[color_groups[k][0] - 1][0].get_color()))
                    if label == 0:
                        lines.append(plt.plot(w, self.DAmodels[i].calc_comp(j + 1, w, self.pararrays[i])))
                else:
                    label = 0
                    for k in range(len(color_groups)):
                        if j + 1 in color_groups[k][1:]:
                            label += 1
                            lines.append(plt.plot(w, self.DAmodels[i].calc_comp(j + 1, w, self.pararrays[i]) + self.DAmodels[i].calc_comp(continuum_base, w, self.pararrays[i]), color = lines[color_groups[k][0] - 1][0].get_color()))
                    if label == 0:
                        lines.append(plt.plot(w, self.DAmodels[i].calc_comp(j + 1, w, self.pararrays[i]) + self.DAmodels[i].calc_comp(continuum_base, w, self.pararrays[i])))

            pdf.savefig()
            plt.clf()


        pdf.close()


    def plot_original_spectra(self):

        pdf = PdfPages("original_spectra.pdf")

        for i in range(len(self.names)):
            l = open(self.names[i]).readlines()
            w = [float(j.split()[0]) for j in l]
            f = [float(j.split()[1]) for j in l]
            (w, f) = np.array((w, f))
            f = f / self.units[i]

            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(w, f, color = "k")
            plt.title(self.names[i])
            plt.xlabel(r"$\mathrm{Wavelength\ (\AA)}$")
            plt.ylabel(r"$\mathrm{Flux\ (\times 10^{%i}\ erg\ s^{-1}\ cm^{-2}\ \AA^{-1})}$" % (np.log10(self.units[i])))

            pdf.savefig()
            plt.clf()


        pdf.close()





            




def main():
    result = DASpec_result('/home/dupu/works/ark120/calibration/new/caha/measure_new/fitting2/list_fit.out.red')
    print result.windows

if __name__ == "__main__":
    main()
