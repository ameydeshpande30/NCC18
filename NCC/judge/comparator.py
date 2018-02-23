import os, sys


def compare(fname1, fname2):
    flag = 0
    if (os.path.isfile(fname1) and os.path.isfile(fname2)):
        # print "in com"
        f1 = open(fname1)
        f2 = open(fname2)
        l = f1.readlines()

        m = f2.readlines()
        if (len(l) == len(m)):
            # print "not same"
            # else:
            for i in range(len(l)):  # check if files of equal length
                if (l[i].strip() == m[i].strip()):
                    flag = 1
                else:
                    flag = 0
                    break
            if (flag == 1):
                # print "same"
                return flag
            else:
                # print "not same"
                flag = -99
                return flag

        return -99
