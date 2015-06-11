from lpsolve55 import *
from pprint import pprint

def powerset(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result], lst, [[]])

supp = powerset([0,1,2,3,4])
supp.remove([])

for s1 in supp:
    for s2 in supp:
        print('================')
        pprint(s1)
        pprint(s2)
        num_coeffs = len(s1)+len(s2)

        lp = lpsolve('make_lp', 0, 12)
        lpsolve('set_verbose', lp, IMPORTANT)
        ret = lpsolve('set_obj_fn', lp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # u v p11 p12 p13 p14 p15 p21 p22 p23 p24 p25
        ret = lpsolve('add_constraint', lp, [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], 'EQ', 1)
        ret = lpsolve('add_constraint', lp, [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], 'EQ', 1)

        for i in s1:
            coeffs = [1, 0] # u
            coeffs.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            for k in range(7, 12): # p2x coeffs
                su_idx = k-7
                if su_idx in s2:
                    if i == su_idx:
                        coeffs[k] = 0
                    else:
                        coeffs[k] = i+1
                else:
                    coeffs[k] = 0
            ret = lpsolve('add_constraint', lp, coeffs, 'EQ', 0)
        for j in s2:
            coeffs = [0, 1] # v
            coeffs.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            for l in range(2, 7): # p2x coeffs
                su_idx = k-2
                if su_idx in s1:
                    if j == su_idx:
                        coeffs[l] = 0
                    else:
                        coeffs[l] = j+1
                else:
                    coeffs[l] = 0
            ret = lpsolve('add_constraint', lp, coeffs, 'EQ', 0)

        ret = lpsolve('set_lowbo', lp, 3, 0)
        ret = lpsolve('set_lowbo', lp, 4, 0)
        ret = lpsolve('set_lowbo', lp, 5, 0)
        ret = lpsolve('set_lowbo', lp, 6, 0)
        ret = lpsolve('set_lowbo', lp, 7, 0)
        ret = lpsolve('set_lowbo', lp, 8, 0)
        ret = lpsolve('set_lowbo', lp, 9, 0)
        ret = lpsolve('set_lowbo', lp, 10, 0)
        ret = lpsolve('set_lowbo', lp, 11, 0)
        ret = lpsolve('set_lowbo', lp, 12, 0)

        lpsolve('solve', lp)
        #print lpsolve('get_objective', lp)
        print lpsolve('get_variables', lp)[0]
        #print lpsolve('get_constraints', lp)[0]
