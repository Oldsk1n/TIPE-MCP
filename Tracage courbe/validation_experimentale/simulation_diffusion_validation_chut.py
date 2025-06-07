import numpy as np
import matplotlib.pyplot as plt

# Paramètres géométriques et physiques
L = 0.09             # épaisseur du mur en m
N = 500              # nombre de points spatiaux
dx = L / (N - 1)    # pas spatial
rho = 800           # masse volumique en kg/m^3
cp = 2200           # capacité thermique sensible en J/(kg.K)
L_latent = 150000   # chaleur latente en J/kg
T_m = 58.0          # température de fusion en °C
delta = 5.0         # intervalle autour de T_m pour le changement de phase (°C)
k = 0.19             # conductivité thermique en W/(m.K)

# Conditions initiales et aux limites
T_initial = 22.3    # température initiale (°C)
T_hot = 90.0        # température imposée à gauche (°C)
T_cold = 0.0       # température imposée à droite (°C)

# Discrétisation temporelle
dt = 0.01           # pas de temps en s
total_time = 2800.0 # temps total de simulation en s
num_steps = int(total_time / dt)
time = np.linspace(0, total_time, num_steps)

# Enregistrement des valeurs
T_milieux = []      # point 250
T_chaud = []        # point 111
T_froid = []       # point 389

# Fonctions de conversion entre température et enthalpie
def compute_H(T):
    H = np.zeros_like(T)
    mask_solid = T < (T_m - delta)
    mask_liquid = T > (T_m + delta)
    mask_mushy = (~mask_solid) & (~mask_liquid)
    
    H[mask_solid] = rho * cp * T[mask_solid]
    H[mask_liquid] = rho * cp * T[mask_liquid] + rho * L_latent
    H[mask_mushy] = rho * cp * T[mask_mushy] + rho * L_latent * ((T[mask_mushy] - (T_m - delta)) / (2 * delta))
    return H

def T_from_H(H):
    T = np.zeros_like(H)
    H_low = rho * cp * (T_m - delta)
    H_high = rho * cp * (T_m + delta) + rho * L_latent
    
    mask_solid = H < H_low
    mask_liquid = H > H_high
    mask_mushy = (~mask_solid) & (~mask_liquid)
    
    T[mask_solid] = H[mask_solid] / (rho * cp)
    T[mask_liquid] = (H[mask_liquid] - rho * L_latent) / (rho * cp)
    T[mask_mushy] = (H[mask_mushy] + (rho * L_latent / (2 * delta)) * (T_m - delta)) / (rho * cp + (rho * L_latent / (2 * delta)))
    return T

# Discrétisation spatiale et conditions initiales
x = np.linspace(0, L, N)
T = np.ones(N) * T_initial
T[0] = T_hot
T[-1] = T_cold
H = compute_H(T)

# Suivi pour affichage
T_record = []
time_record = []
interface_positions = []

# Boucle temporelle (schéma explicite)
for n in range(num_steps):
    T = T_from_H(H)
    T_chaud.append(T[150])
    T_milieux.append(T[250])
    T_froid.append(T[350])
    
    d2Tdx2 = np.zeros_like(T)
    d2Tdx2[1:-1] = (T[2:] - 2 * T[1:-1] + T[:-2]) / dx**2
    
    H_new = H.copy()
    H_new[1:-1] = H[1:-1] + dt * k * d2Tdx2[1:-1]
    
    H_new[0] = compute_H(np.array([T_hot]))[0]
    H_new[-1] = compute_H(np.array([T_cold]))[0]
    
    H = H_new.copy()

    # Suivi de l'interface solide/liquide
    mushy_zone = (T >= (T_m - delta)) & (T <= (T_m + delta))
    if np.any(mushy_zone):
        idxs = np.where(mushy_zone)[0]
        i1 = idxs[0]
        if i1 < N - 1:
            T1, T2 = T[i1], T[i1+1]
            x1, x2 = x[i1], x[i1+1]
            if T2 != T1:
                x_interface = x1 + (T_m - T1) * (x2 - x1) / (T2 - T1)
            else:
                x_interface = x1
            interface_positions.append(x_interface)
            time_record.append(n * dt)

    # Stockage pour affichage des profils
    if n % 1000 == 0:
        T_record.append(T.copy())


# %%

releve_chaud = open("relevé_chaud_chut.csv","r",encoding="latin-1")
releve_milieu = open("relevé_milieu_chut.csv","r",encoding="latin-1")
releve_froid = open("relevé_froid_chut.csv","r",encoding="latin-1")

releve_chaud.readline()
releve_milieu.readline()
releve_froid.readline()

T_chaud_exp = []
T_milieu_exp = []
T_froid_exp = []
temps = []

for line in releve_chaud:
    
    line = line.rstrip('\n')
    line = line.split(';')
    
    t = float(line[0].replace(",", "."))    
    T = float(line[1].replace(",", "."))
    
    temps.append(t)
    T_chaud_exp.append(T)
    
for line in releve_milieu:
    
    line = line.rstrip('\n')
    line = line.split(';')
    
    t = float(line[0].replace(",", "."))    
    T = float(line[1].replace(",", "."))
    
    T_milieu_exp.append(T)
    
for line in releve_froid:
    
    line = line.rstrip('\n')
    line = line.split(';')
    
    t = float(line[0].replace(",", "."))    
    T = float(line[1].replace(",", "."))

    T_froid_exp.append(T)
    

# %%
y_err_chaud = [1]*len(T_chaud_exp)
y_err_milieu = [1]*len(T_milieu_exp)
y_err_froid = [1]*len(T_froid_exp)

plt.figure(figsize=(8, 5))
plt.plot(temps,T_chaud_exp,marker='o',linestyle='none',label='relevé expérimental')
plt.errorbar(
    temps,       # abscisses où afficher les barres
    T_chaud_exp,     # ordonnées correspondantes
    yerr=y_err_chaud,       # incertitude (hauteur d'erreur)
    fmt='none',                
    capsize=4,        # longueur des « chapeaux » au sommet des barres
    label="Incertitudes (±1 K)"
)
plt.plot(time, T_chaud,label='modèle numérique')
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Évolution de la température coté chaud")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(temps,T_froid_exp,marker='o',linestyle='none',label='relevé expérimental')
plt.errorbar(
    temps,       # abscisses où afficher les barres
    T_froid_exp,     # ordonnées correspondantes
    yerr=y_err_froid,       # incertitude (hauteur d'erreur)
    fmt='none',                
    capsize=4,        # longueur des « chapeaux » au sommet des barres
    label="Incertitudes (±1 K)"
)
plt.plot(time, T_froid,label='modèle numérique')
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Évolution de la température coté froid")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(temps,T_milieu_exp,marker='o',linestyle='none',label='relevé expérimental')
plt.errorbar(
    temps,       # abscisses où afficher les barres
    T_milieu_exp,     # ordonnées correspondantes
    yerr=y_err_milieu,       # incertitude (hauteur d'erreur)
    fmt='none',                
    capsize=4,        # longueur des « chapeaux » au sommet des barres
    label="Incertitudes (±1 K)"
)
plt.plot(time, T_milieux,label='modèle numérique')
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.title("Évolution de la température au centre")
plt.grid(True)
plt.show()