#!/usr/bin/env python

def DASpec_reduce(filename):
    l = open(filename).readlines()
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

    
    output = open(sys.argv[1] + '.red', 'w')
    for i in xrange(len(index_tot)):
        #print index_tot[i][0], end_tot[i]
        for j in range(index_tot[i][0], end_tot[i] + 1):
            output.write(l[j])
    output.close()
        

if __name__ == '__main__':
    import sys
    DASpec_reduce(sys.argv[1])
