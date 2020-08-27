#!/usr/bin/env python

import numpy as np
import DASpec
import DASpec_extract_result
import matplotlib.pyplot as plt

def main():

    # === read spectrum file
    l = open("20200217_forDASpec.txt").readlines()
    w = [float(i.split()[0]) for i in l]
    f = [float(i.split()[1]) for i in l]
    e = [float(i.split()[2]) for i in l]
    (w, f, e) = np.array((w, f, e))

    # === read fitting result
    result = DASpec_extract_result.DASpec_result("20200217_forDASpec.txt.out.red")
    
    # === create a model
    model = DASpec.compcontainer()
    for i in xrange(len(result.models[0])):
        model.add(eval('DASpec.' + result.models[0][i]))

    # === begin plot
    plt.plot(w, f)
    for i in xrange(len(result.models[0])):
        c = model.calc_comp(i + 1, w, result.pararrays[0]) # component of the result
        plt.plot(w, c * result.units[0])
    s = model.calc(w, result.pararrays[0]) # total fitting result
    plt.plot(w, s * result.units[0])

    plt.show()
    

    

if __name__ == '__main__':
    main()