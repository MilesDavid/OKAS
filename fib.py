#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import decimal
import numpy as np

def fib(N):
    if N <= 0:
        return
    elif N <= 2:
        return 1

    fn = fn1 = 1

    for i in range(2, N):
        tmp = fn1
        fn1 += fn
        fn = tmp

    return fn1

def fib_matrix(N):
    if N <= 0:
        return
    elif N <= 2:
        return 1

    """
        [[  Fn+1, Fn    ],      [[  1,  1   ], ** n
            Fn,   Fn-1  ]]  ==      1,  0   ]]
    """

    N -= 1
    pows = set()

    i = 0
    while N > 1:
        if N % 2:
            pows.add(i)
        N //= 2
        i += 1

    pows.add(i)

    m1 = np.matrix([[1, 1], [1, 0]], np.dtype(decimal.Decimal))
    factors = []

    for i in pows:
        m = m1.copy()
        m = m ** (2 ** i)

        factors.append(m)

    if factors:
        res_matrix = 1
        for factor in factors:
            res_matrix *= factor

        return res_matrix[0, 0]
