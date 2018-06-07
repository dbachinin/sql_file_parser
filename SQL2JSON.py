#! /usr/bin/python
# -*- coding: UTF-8 -*-

import re, os, sys, json

data = []

for line in open('./dump.sql'):
    li = line.strip()
    if not (li.startswith("/") or li.startswith("--")):
        data.append(line.strip())
names = []
for stroke in data:
    if "INSERT INTO" in stroke:
        names.append(stroke.split(' ')[2].replace('`',''))
def find_tuple(name,findby,value):
    for i in range(0,len(out[name])):
        if out[name][i][findby] == value:
            return out[name][i]

def get_ids(name):
    exec("%s = []" % (name))
    for st in data:
        if ("INSERT INTO `{}`".format(name)) in st:
            for i in re.findall("\((.*?)\)",st):
                sttemp = re.split("\,(?=(?:[^']*'[^']*')*[^']*$)",i)
                exec("%s.append(sttemp)" % (name))
    exec("out = %s" % (name))
    head = []
    for item in out[0]:
        head.append(re.findall("`.*?`",item)[0].replace('`',''))
        out[0] = head
    exec("%s_json = {}" % (name))
    exec("%s_json['%s'] = []" % (name,name))
    for element in range(1,len(out)):
        exec("%s_json['%s'].append(json.loads(json.dumps(dict(zip(out[0],out[element])))))" % (name,name))
        exec("out_json = %s_json" % (name))
    return out_json
out = {}
for name in names:
    out.update(get_ids(name))
os.remove('/tmp/tmp')
with open('/tmp/tmp.json', 'w') as f:
    json.dump(out, f)

