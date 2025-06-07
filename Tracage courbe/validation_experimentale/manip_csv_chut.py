import numpy as np
fichier = open("releve_texte.txt","r",encoding="latin-1")

releve_1 = open("relevé_1.csv","w",encoding="latin-1")
releve_2 = open("relevé_2.csv","w",encoding="latin-1")
releve_3 = open("relevé_3.csv","w",encoding="latin-1")
t1 = []
t2 = []
t3 = []
releve_1_list = []
releve_2_list = []
releve_3_list = []


for line in fichier :
    line = line.rstrip("\n")
    elements = line.split(";")
    t1.append(elements[0])
    t2.append(elements[2])
    t3.append(elements[4])
    releve_1_list.append(elements[1])
    releve_2_list.append(elements[3])
    releve_3_list.append(elements[5])
    
indice1 = np.arange(0,len(t1),20)
indice2 = np.arange(0,len(t2),20)
indice3 = np.arange(0,len(t3),20)

for i in indice1:
    releve_1.write(t1[i] + ";" + releve_1_list[i] + "\n")
    
for i in indice2:
    releve_2.write(t2[i] + ";" + releve_2_list[i] + "\n")

for i in indice3:
    releve_3.write(t1[i] + ";" + releve_3_list[i] + "\n")


fichier.close()
releve_1.close()
releve_2.close()
releve_3.close()