import matplotlib.pyplot as plt
import numpy as np

def T_ext(t):
    # Moyenne 20 °C, amplitude 10 °C
    if 0<=t<5400 or 10800<=t<=16200:
        return 80
    else:
        return 20
    

def plot_courbe(file_to_plot, name_curve):
    # Lecture du fichier
    with open(file_to_plot, 'r') as f:
        text = f.readlines()

    t = []
    deg = []
    temp_ext = []
    text.readline()

    for line in text:
        x, y = line.split(',')
        if est_convertible_en_float(x) and est_convertible_en_float(y):
            t_i = float(x)
            deg_i = float(y)
            t.append(t_i)
            deg.append(deg_i)
            temp_ext.append(T_ext(t_i))

    # Conversion en tableau NumPy (optionnel mais pratique)
    t    = np.array(t)
    deg  = np.array(deg)
    temp_ext = np.array(temp_ext)

    # On choisit un intervalle fixe (ici tous les 20 points)
    interval = 50
    indices = np.arange(0, len(t), interval)

    # Définir l'incertitude (même constante pour chaque point sélectionné)
    y_err = np.ones_like(indices)  # tableau de 1 pour chaque point d'erreur

    # Tracé des deux courbes
    plt.plot(t, temp_ext, label="Température extérieure", linestyle='--')
    plt.plot(t, deg,       label="Température intérieure")

    # Barres d'erreur verticales uniquement aux points t[indices]
    plt.errorbar(
        t[indices],       # abscisses où afficher les barres
        deg[indices],     # ordonnées correspondantes
        yerr=y_err,       # incertitude (hauteur d'erreur)
        fmt='none',                
        capsize=4,        # longueur des « chapeaux » au sommet des barres
        label="Incertitudes (±1 °C)"
    )

    plt.title(name_curve)
    plt.xlabel("Temps (secondes)")
    plt.ylabel("Température (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def est_convertible_en_float(valeur):
    try:
        float(valeur)
        return True  # La conversion a réussi
    except ValueError:
        return False  # La conversion a échoué
