#!/usr/bin/env python

import sys

def check_model(filename):
    """ check if the models are the same for all of the objects """
    index = []
    model = []
    
    l = open(filename).readlines()
    sep = [i[0] for i in zip(range(len(l)), l) if '####' in i[1]]

    models = []
    for i in xrange(len(sep)):
        x = sep[i] + 1
        while 1:
            if l[x][0] == '#' and l[x].split()[1] == 'model:':
                break
            else:
                x += 1
        y = x + 1
        while 1:
            if l[x][0] == '#' and l[x].split()[1] == 'fix:':
                break
            else:
                x += 1
        z = x + 0
        model_i = l[y: z]
        models.append(model_i)

    label = 0
    for i in xrange(len(models) - 1):
        if models[0] != models[i + 1]:
            print 'model not the same: %i' % (i + 1)
            label == 1
    if label == 0:
        print 'check model ok!'
    else:
        print 'check model failed!'
        sys.exit()

def extract_par_all(filename):

    l = open(filename).readlines()
    sep = [i[0] for i in zip(range(len(l)), l) if '####' in i[1]]

    par_errs = []
    for i in xrange(len(sep)):
        name = l[sep[i] + 1].split('\n')[0]
        print name,

        x = sep[i] + 1
        while 1:
            if l[x][0] == '#' and l[x].split()[1] == 'unit:':
                unit = float(l[x + 1].split('\n')[0])
                break
            else:
                x += 1
        print 'unit:', unit,

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

        par_i = [i.split(':')[1].split('\n')[0].split() for i in par_i]
        err_i = [i.split(':')[1].split('\n')[0].split() for i in err_i]
        #print par_i
        #print err_i

        #for j in xrange(len(comp)):
        #    print par_i[comp[j] - 1][par[j] - 1], err_i[comp[j] - 1][par[j] - 1],
        #print 
        for j in xrange(len(par_i)):
            for k in xrange(len(par_i[j])):
                print par_i[j][k], err_i[j][k],
        print


if __name__ == "__main__":
    filename = sys.argv[1]
    #comp_par = [int(i) for i in sys.argv[2:]]
    #print 'comp_par:', comp_par
    check_model(filename)
    extract_par_all(filename)
