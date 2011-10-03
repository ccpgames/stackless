#!/usr/bin/python
# Usage: typeslots.py < Include/typeslots.h > typeslots.inc

import sys, re

print("/* Generated by typeslots.py $Revision: 87806 $ */")
res = {}
for line in sys.stdin:
    m = re.match("#define Py_([a-z_]+) ([0-9]+)", line)
    if not m:
        continue
    member = m.group(1)
    if member.startswith("tp_"):
        member = "ht_type."+member
    elif member.startswith("nb_"):
        member = "as_number."+member
    elif member.startswith("mp_"):
        member = "as_mapping."+member
    elif member.startswith("sq_"):
        member = "as_sequence."+member
    elif member.startswith("bf_"):
        member = "as_buffer."+member
    res[int(m.group(2))] = member

HTPREFIX = "ht_type."
M = max(res.keys())+1
for i in range(1,M):
    if i in res:
        if res[i].startswith(HTPREFIX):
            print("#ifdef STACKLESS")
            print("  offsetof(PyHeapTypeObject, %s)," % res[i][len(HTPREFIX):])
            print("#else")
            print("  offsetof(PyHeapTypeObject, %s)," % res[i])
            print("#endif")
        else:
            print("offsetof(PyHeapTypeObject, %s)," % res[i])
    else:
        print("0,")
