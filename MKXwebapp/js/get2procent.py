#!/usr/bin/env python
# encoding: utf-8

import sys

f = open('latlngs2procent.js', 'r')
i = 0
while f:
    line = f.readline()
    if not line:
        break
    i = i + 1
    if (i % 50 == 0):
        print line,
f.close()