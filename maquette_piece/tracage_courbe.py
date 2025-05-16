import matplotlib.pyplot as plt

# %%
def plot_courbe(file_to_plot):
     
     file = open(file_to_plot,'r')
     text = file.readlines() 
     deg = []
     t = []
     
     for line in text :
         x , y = line.split(',')
         if est_convertible_en_float(x) == True and est_convertible_en_float(y) == True :
             t.append(float(x))
             deg.append(float(y))
         
     plt.plot(t , deg, )
     plt.show
# %%

def est_convertible_en_float(valeur):
    try:
        float(valeur)
        return True  # La conversion a réussi
    except ValueError:
        return False  # La conversion a échoué