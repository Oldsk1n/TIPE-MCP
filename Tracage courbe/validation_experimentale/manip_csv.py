fichier = open("releve_texte.txt","r",encoding="latin-1")

releve_1 = open("relevé_1.csv","w",encoding="latin-1")
releve_2 = open("relevé_2.csv","w",encoding="latin-1")
releve_3 = open("relevé_3.csv","w",encoding="latin-1")

for line in fichier :
    line = line.rstrip("\n")
    elements = line.split(";")
    releve_1.write(elements[0] + ";" + elements[1] + "\n")
    releve_2.write(elements[2] + ";" + elements[3] + "\n")
    releve_3.write(elements[4] + ";" + elements[5] + "\n")

fichier.close()
releve_1.close()
releve_2.close()
releve_3.close()
# %%



