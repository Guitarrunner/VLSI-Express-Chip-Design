from pathlib import Path

txt = Path('C:/Users/toshi/Downloads/Level up/VLSI-Express-Chip-Design/log.txt').read_text()


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
    
print(txt1)
