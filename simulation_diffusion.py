import numpy as np
import matplotlib.pyplot as plt

# Paramètres géométriques et physiques
L = 0.1             # épaisseur du mur en m
N = 50             # nombre de points spatiaux
dx = L / (N - 1)    # pas spatial
rho = 800           # masse volumique en kg/m^3
cp = 2000           # capacité thermique sensible en J/(kg.K)
L_latent = 150000   # chaleur latente en J/kg
T_m = 30.0          # température de fusion en °C
delta = 1.0         # intervalle autour de T_m pour le changement de phase (°C)
k = 0.5             # conductivité thermique en W/(m.K)

# Conditions initiales et aux limites
T_initial = 20.0    # température initiale (°C)
T_hot = 40.0        # température imposée à gauche (°C)
T_cold = 20.0       # température imposée à droite (°C)

# Discrétisation temporelle
dt = 0.01          # pas de temps en s
total_time = 3600.0   # temps total de simulation en s
num_steps = int(total_time / dt)

# Fonctions de conversion entre température et enthalpie

def compute_H(T):
    """
    Calcule l'enthalpie H pour une température T donnée.
    """
    H = np.zeros_like(T)
    # Zone solide
    mask_solid = T < (T_m - delta)
    # Zone liquide
    mask_liquid = T > (T_m + delta)
    # Zone de transition (région mushy)
    mask_mushy = (~mask_solid) & (~mask_liquid)
    
    H[mask_solid] = rho * cp * T[mask_solid]
    H[mask_liquid] = rho * cp * T[mask_liquid] + rho * L_latent
    H[mask_mushy] = rho * cp * T[mask_mushy] + rho * L_latent * ((T[mask_mushy] - (T_m - delta)) / (2 * delta))
    return H

def T_from_H(H):
    """
    Calcule la température T à partir de l'enthalpie H.
    """
    T = np.zeros_like(H)
    # Enthalpie correspondant à T = T_m - delta et T = T_m + delta
    H_low = rho * cp * (T_m - delta)
    H_high = rho * cp * (T_m + delta) + rho * L_latent
    
    mask_solid = H < H_low
    mask_liquid = H > H_high
    mask_mushy = (~mask_solid) & (~mask_liquid)
    
    T[mask_solid] = H[mask_solid] / (rho * cp)
    T[mask_liquid] = (H[mask_liquid] - rho * L_latent) / (rho * cp)
    
    # Dans la région mushy, la relation est linéarisée :
    # H = rho*cp*T + rho*L_latent * (T - (T_m-delta))/(2*delta)
    # d'où : T = (H + (rho*L_latent/(2*delta))*(T_m-delta)) / (rho*cp + rho*L_latent/(2*delta))
    T[mask_mushy] = (H[mask_mushy] + (rho * L_latent / (2 * delta)) * (T_m - delta)) / (rho * cp + (rho * L_latent / (2 * delta)))
    return T

# Discrétisation spatiale et conditions initiales
x = np.linspace(0, L, N)
T = np.ones(N) * T_initial
T[0] = T_hot
T[-1] = T_cold

# Calcul initial de l'enthalpie à partir de T
H = compute_H(T)

# Stockage des profils de température pour affichage
T_record = []
time_record = []

# Boucle temporelle (schéma explicite)
for n in range(num_steps):
    # On déduit T à partir de H
    T = T_from_H(H)
    
    # Calcul de la dérivée seconde de T par différences finies
    d2Tdx2 = np.zeros_like(T)
    d2Tdx2[1:-1] = (T[2:] - 2 * T[1:-1] + T[:-2]) / dx**2
    
    # Mise à jour de l'enthalpie H en chaque point intérieur
    H_new = H.copy()
    H_new[1:-1] = H[1:-1] + dt * k * d2Tdx2[1:-1]
    
    # Réimposition des conditions aux limites (en forçant T, puis conversion en H)
    H_new[0] = compute_H(np.array([T_hot]))[0]
    H_new[-1] = compute_H(np.array([T_cold]))[0]
    
    H = H_new.copy()
    
"""    # Enregistrement de quelques profils pour affichage
    if n % 1000 == 0:
        T_record.append(T.copy())
        time_record.append(n * dt)

# Visualisation des résultats
plt.figure(figsize=(8, 5))
for idx, T_profile in enumerate(T_record):
    plt.plot(x, T_profile, label=f"t = {time_record[idx]:.2f} s")"""
plt.plot(x, T)
plt.xlabel("Distance (m)")
plt.ylabel("Température (°C)")
plt.title("Simulation enthalpique de diffusion thermique avec PCM")
plt.legend()
plt.grid(True)
plt.show()
