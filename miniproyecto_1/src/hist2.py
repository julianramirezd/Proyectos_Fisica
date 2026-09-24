import random
import matplotlib.pyplot as plt

# Parámetros del sistema
N = 4
sigma = 0.1197
sigma_sq = sigma ** 2
delta = 0.1  # Amplitud del paso de Metropolis
n_steps = 2000000  # Pasos requeridos (2 x 10^6)

# Estado inicial no solapado
L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]

histo_data_mcmc = []

for step in range(n_steps):
    # Selecciona una partícula al azar y propone movimiento
    a = random.choice(L)
    b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
    
    # Condición de paredes y choque entre discos
    box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
    min_dist_sq = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
    
    # Criterio de aceptación
    if not (box_cond or min_dist_sq < 4.0 * sigma_sq):
        a[:] = b

    # Guardar las coordenadas X de las partículas en el estado actual
    for k in range(N):
        histo_data_mcmc.append(L[k][0])

# Generación del Histograma
plt.figure(figsize=(8, 5))
plt.hist(histo_data_mcmc, bins=100, density=True, color='green', alpha=0.7)
plt.xlabel('x')
plt.ylabel('frequency')
plt.title('Markov Chain Sampling: x coordinate histogram (eta=0.18)')
plt.grid(True)
plt.savefig('miniproyecto_1/figures/mcmc_disks_histo.png')
plt.show()