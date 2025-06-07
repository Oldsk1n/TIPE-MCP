import matplotlib.pyplot as plt
import numpy as np
# %%
def T_ext(t):
    # Moyenne 20 °C, amplitude 10 °C
    if 0<=t<5400 or 10800<=t<=16200:
        return 80
    else:
        return 20
    
def plot_courbe(file_to_plot, name_curve):
     
     file = open(file_to_plot,'r')
     text = file.readlines() 
     deg = []
     t = []
     temp_ext = []
     
     for line in text :
         x , y = line.split(',')
         if est_convertible_en_float(x) == True and est_convertible_en_float(y) == True :
             t.append(float(x))
             deg.append(float(y))
             temp_ext.append(T_ext(float(x)))
             
     indices = np.arange(0,len(t), 20)
     y_err = [1]*len(indices)
    
     plt.plot(t, temp_ext, label= "température extérieure",linestyle = '--')
     plt.plot(t , deg, label = "température intérieure")
     plt.errorbar(t[indices], deg[indices], yerr=y_err)
     plt.title(name_curve)
     plt.xlabel("temps en seconde")
     plt.ylabel("Température en dégré Celcius")
     plt.show
# %%

def est_convertible_en_float(valeur):
    try:
        float(valeur)
        return True  # La conversion a réussi
    except ValueError:
        return False  # La conversion a échoué
    