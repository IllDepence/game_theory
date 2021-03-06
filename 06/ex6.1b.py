#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lpsolve55 import *
from pprint import pprint

def powerset(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result], lst, [[]])

supp = powerset([0,1,2,3,4])
supp.remove([])

for s1 in supp:
    for s2 in supp:
        num_coeffs = len(s1)+len(s2)

        lp = lpsolve('make_lp', 0, 12)
        lpsolve('set_verbose', lp, IMPORTANT)

        # u v p11 p12 p13 p14 p15 p21 p22 p23 p24 p25
        ret = lpsolve('set_obj_fn', lp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        ret = lpsolve('add_constraint', lp, [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], 'EQ', 1)
        ret = lpsolve('add_constraint', lp, [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], 'EQ', 1)

        # p11 - p15
        for i in range(0, 5):
            # u - U_1 ... (defaults)
            coeffs = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for y in range(1, 6):
                x = i+1
                if not x == y:
                    coeffs[y+6] = -x
                ret = lpsolve('add_constraint', lp, coeffs, 'GE', 0)
            # support set specific
            if i in s1:
                # u - U_1 ...
                coeffs = [1, 0] # u
                coeffs.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                for k in range(7, 12): # p2x coeffs
                    su_idx = k-7
                    if su_idx in s2:
                        if i == su_idx:
                            coeffs[k] = 0
                        else:
                            coeffs[k] = -(i+1)
                    else:
                        coeffs[k] = 0
                ret = lpsolve('add_constraint', lp, coeffs, 'EQ', 0)
            else:
                # α(p.) = 0
                coeffs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                coeffs[i+2] = 1
                ret = lpsolve('add_constraint', lp, coeffs, 'EQ', 0)
        # p21 - p25
        for j in range(0, 5):
            # v - U_2 ... (defaults)
            coeffs = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for y in range(1, 6):
                x = j+1
                if not x == y:
                    coeffs[y+1] = -x
                ret = lpsolve('add_constraint', lp, coeffs, 'GE', 0)
            # support set specific
            if j in s2:
                # v - U_2 ...
                coeffs = [0, 1] # v
                coeffs.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                for l in range(2, 7): # p2x coeffs
                    su_idx = l-2
                    if su_idx in s1:
                        if j == su_idx:
                            coeffs[l] = 0
                        else:
                            coeffs[l] = -(j+1)
                    else:
                        coeffs[l] = 0
                ret = lpsolve('add_constraint', lp, coeffs, 'EQ', 0)
            else:
                # β(p.) = 0
                coeffs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                coeffs[j+7] = 1
                ret = lpsolve('add_constraint', lp, coeffs, 'EQ', 0)

        status = lpsolve('solve', lp)
        if status == 0L:
            print('===== optimal solution =====')
            result = lpsolve('get_variables', lp)[0]
            print('u: {0}'.format(result[0]))
            print('v: {0}'.format(result[1]))
            for i in s1:
                print('α(p{0}): {1}'.format(i+1, result[i+2]))
            for j in s2:
                print('β(p{0}): {1}'.format(j+1, result[j+7]))
