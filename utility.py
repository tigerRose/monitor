#!/usr/bin/env python
# -*- coding: utf-8 -*-

def my_bin(i, l=8):
    i = bin(i)[2:]
    if len(i) < l:
        return '0'*(l-len(i))+i
    return i

def my_hex(i, is_reverse=False, l=4):
    i = hex(i)[2:].upper()
    if len(i) < l:
        i = '0'*(l-len(i))+i

    if is_reverse:
        i = i[len(i)/2:] + i[:len(i)/2]

    return i
