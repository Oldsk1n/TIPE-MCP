import matplotlib.pyplot as plt
import numpy as np

def plot_courbe(file_to_plot, name_curve):
    # Lecture du fichier
    text = open(file_to_plot, 'r', encoding='latin-1')

    t = []
    deg = []
    text.readline()

    for line in text:
        line = line.rstrip("\n").split(";")
        x = float(line[0].replace(",", "."))    # convertir en float
        y = float(line[1].replace(",", "."))    # convertir en float
        if est_convertible_en_float(x) and est_convertible_en_float(y):
            t_i = float(x)
            deg_i = float(y)
            t.append(t_i)
            deg.append(deg_i)

    # Conversion en tableau NumPy (optionnel mais pratique)
    t    = np.array(t)
    deg  = np.array(deg)

    # On choisit un intervalle fixe (ici tous les 20 points)
    interval = 50
    indices = np.arange(0, len(t), interval)

    # Définir l'incertitude (même constante pour chaque point sélectionné)
    y_err = np.ones_like(indices)  # tableau de 1 pour chaque point d'erreur

    # Tracé des deux courbes
    plt.plot(t, deg,label="Température de l'échantillon")

    # Barres d'erreur verticales uniquement aux points t[indices]
    plt.errorbar(
        t[indices],       # abscisses où afficher les barres
        deg[indices],     # ordonnées correspondantes
        yerr=y_err,       # incertitude (hauteur d'erreur)
        fmt='none',                
        capsize=4,        # longueur des « chapeaux » au sommet des barres
        label="Incertitudes (±1 K)"
    )

    plt.title(name_curve)
    plt.xlabel("Temps (secondes)")
    plt.ylabel("Température (K)")
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