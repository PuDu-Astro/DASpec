#!/usr/bin/env python2

import sys
import DASpec_extract_result
import DASpec
import numpy as np
import matplotlib.pyplot as plt

def check_models(models):

    model0 = models[0]

    for i in xrange(len(models) - 1):
        label = 0
        # print False in model0 == models[i + 1]
        index = model0 == models[i + 1]
        index = np.where(True == index)
        # print len(index[0]), len(model0)
        if len(index[0]) != len(model0):
            label += 1
        if label != 0:
            print "ERROR!! components not the same!!! num:", i + 1
            sys.exit()
            

def main():

    resname = sys.argv[1]
    comp = [int(i) for i in sys.argv[2:]]

    output = open("sub_comp.txt", 'w')
    for i in comp:
        output.write("%i " % i)
    output.write("\n")
    output.close()

    res = DASpec_extract_result.DASpec_result(resname)

    check_models(res.models)

    for i in res.models[0]:
        print i

    model = DASpec.compcontainer()
    for i in xrange(len(res.models[0])):
        eval("model.add(DASpec." + res.models[0][i] + ")")
    
    model.info()

    for j in xrange(len(res.names)):
    # for j in xrange(1):
        l = open(res.names[j]).readlines()

        w = [float(i.split()[0]) for i in l]
        f = [float(i.split()[1]) for i in l]
        e = [float(i.split()[2]) for i in l]

        t = model.calc(w, res.pararrays[j])
        t2 = np.zeros(len(w))

        for k in xrange(len(res.models[j])):
            if k + 1 in comp:
                t2 = t2 + model.calc_comp(k + 1, w, res.pararrays[j])

        output = open(res.names[j] + ".sub", 'w')
        for m in xrange(len(w)):
            text = "%f  %e  %e\n" % (w[m], f[m] - t2[m] * res.units[j], e[m])
            output.write(text)
        output.close()

        # plt.plot(w, f)
        # plt.plot(w, t * res.units[j])
        # plt.plot(w, t2 * res.units[j])
        # plt.show()


if __name__ == "__main__":
    main()