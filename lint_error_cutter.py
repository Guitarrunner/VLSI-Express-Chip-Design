# Imports
from pathlib import Path

from fabric.utils import error

# Data treatment
txt = Path('log.txt').read_text()
txt1=txt.split('\n')
txt1=txt1[:-1]

for i in range(len(txt1)):
    cutter_twopoint = txt1[i].find(":")
    txt1[i]=txt1[i][cutter_twopoint+1:]
    cutter_twopoint = txt1[i].find(": ")
    if txt1[i].find(" [") != -1:
        cutter_parenthesis =  txt1[i].find(" [")
    if txt1[i].find(" (syntax-error)")!=-1:
        cutter_parenthesis = txt1[i].find(" (syntax-error)")
    
    temp = txt1[i][cutter_twopoint+1:cutter_parenthesis]
    txt1[i]= [txt1[i][:cutter_twopoint],temp]

# Summary of errors
errorList = []
for i in range(len(txt1)):
    if txt1[i][1] not in errorList:
        errorList.append(txt1[i][1])

summary = []
for error in errorList:
    tmp = 0
    for i in range(len(txt1)):
        if txt1[i][1] == error:
            tmp += 1
    summary.append([tmp,error])

open("summary.txt","w").close()
f = open("summary.txt","a")
for i in range(len(summary)):
    f.write("La regla '" + summary[i][1] + "' se está violando " + str(summary[i][0]) + " veces\n")
f.close()

print("[INFO] Summary created")

# Overwrite data in log.txt
errorsCount = 0
open("log.txt","w").close()
f = open("log.txt","a")
for i in range(len(txt1)):
    f.write(txt1[i][0] + txt1[i][1] + "\n")
    errorsCount += 1
f.close()

print("[INFO] Log.txt updated")
