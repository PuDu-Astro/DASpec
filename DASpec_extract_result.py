#!/usr/bin/env python

import sys
import numpy as np

class DASpec_result:

    def __init__(self, filename):
        self.filename = filename
        self.info_txt = open(self.filename).readlines()

        self.names = []
        self.units = []
        self.windows = []
        self.models = []
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


def main():
    result = DASpec_result('/home/dupu/works/ark120/calibration/new/caha/measure_new/fitting2/list_fit.out.red')
    print result.windows

if __name__ == "__main__":
    main()
