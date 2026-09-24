import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==========================================
# 1. PARÁMETROS DEL SISTEMA
# ==========================================
N = 4
sigma = 0.1197
sigma_sq = sigma**2
delta = 0.1  # Paso de Metropolis
del_xy = 0.05  # Tolerancia para caja de Hits

# Configuración de Referencia A
conf_A = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]


def es_hit(pos, target, del_xy):
    """Verifica si la configuración actual está dentro de la caja de tolerancia de A."""
    for p in pos:
        match = False
        for t in target:
            if abs(p[0] - t[0]) < del_xy and abs(p[1] - t[1]) < del_xy:
                match = True
                break
        if not match:
            return False
    return True


# ==========================================
# 2. SIMULACIÓN: MUESTREO DIRECTO
# ==========================================
def simular_directo(n_runs):
    hits_acumulados = np.zeros(n_runs, dtype=int)
    hits = 0

    for i in range(n_runs):
        overlap = True
        while overlap:
            L = [
                (
                    np.random.uniform(sigma, 1.0 - sigma),
                    np.random.uniform(sigma, 1.0 - sigma),
                )
            ]
            for k in range(1, N):
                a = (
                    np.random.uniform(sigma, 1.0 - sigma),
                    np.random.uniform(sigma, 1.0 - sigma),
                )
                min_dist_sq = min(
                    (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for b in L
                )
                if min_dist_sq < 4.0 * sigma_sq:
                    overlap = True
                    break
                else:
                    overlap = False
                    L.append(a)

        if es_hit(L, conf_A, del_xy):
            hits += 1

        hits_acumulados[i] = hits

    pasos = np.arange(1, n_runs + 1)
    prob_estimada = hits_acumulados / pasos
    return pasos, prob_estimada, hits


# ==========================================
# 3. SIMULACIÓN: CADENAS DE MARKOV (MCMC)
# ==========================================
def simular_mcmc(n_steps):
    hits_acumulados = np.zeros(n_steps, dtype=int)
    hits = 0
    L = [list(p) for p in conf_A]  # Estado inicial

    for i in range(n_steps):
        idx = np.random.randint(0, N)
        a = L[idx]
        b = [
            a[0] + np.random.uniform(-delta, delta),
            a[1] + np.random.uniform(-delta, delta),
        ]

        box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
        min_dist_sq = min(
            (b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a
        )

        if not (box_cond or min_dist_sq < 4.0 * sigma_sq):
            L[idx] = b

        if es_hit(L, conf_A, del_xy):
            hits += 1

        hits_acumulados[i] = hits

    pasos = np.arange(1, n_steps + 1)
    prob_estimada = hits_acumulados / pasos
    return pasos, prob_estimada, hits


# ==========================================
# 4. EJECUCIÓN Y COMPARACIÓN DE RENDIMIENTO
# ==========================================
N_MUESTRAS = int(1e6)

print("Corriendo Muestreo Directo...")
t0 = time.time()
pasos_dir, prob_dir, hits_dir = simular_directo(N_MUESTRAS)
t_dir = time.time() - t0

print("Corriendo Cadenas de Markov (MCMC)...")
t0 = time.time()
pasos_mcmc, prob_mcmc, hits_mcmc = simular_mcmc(N_MUESTRAS)
t_mcmc = time.time() - t0

# ==========================================
# 5. GRÁFICOS DE COMPARACIÓN Y FLUCTUACIONES
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Gráfico 1: Convergencia de la Probabilidad Estimada
axes[0].plot(
    pasos_dir,
    prob_dir,
    label=f"Muestreo Directo (Hits={hits_dir})",
    alpha=0.8,
    color="blue",
)
axes[0].plot(
    pasos_mcmc,
    prob_mcmc,
    label=f"MCMC Metropolis (Hits={hits_mcmc})",
    alpha=0.8,
    color="orange",
)
axes[0].set_title(
    "Convergencia de Probabilidad $\hat{P}(A)$ vs. Número de Pasos",
    fontweight="bold",
)
axes[0].set_xlabel("Número de Pasos / Intentos")
axes[0].set_ylabel("Probabilidad Estimada $\hat{P}$")
axes[0].set_xscale("log")
axes[0].legend()
axes[0].grid(True, which="both", ls="--")

# Gráfico 2: Error Relativo (Fluctuaciones Estocásticas)
# El error teórico decrece como 1 / sqrt(N)
error_dir = np.sqrt(prob_dir * (1 - prob_dir) / pasos_dir)
error_mcmc = np.sqrt(prob_mcmc * (1 - prob_mcmc) / pasos_mcmc)

axes[1].plot(
    pasos_dir, error_dir, label="Error Estándar (Directo)", color="blue"
)
axes[1].plot(
    pasos_mcmc,
    error_mcmc,
    label="Error Estándar (MCMC)",
    color="orange",
    linestyle="--",
)
axes[1].set_title(
    "Escalamiento del Error Estándar (Fluctuaciones $\propto 1/\sqrt{N}$)",
    fontweight="bold",
)
axes[1].set_xlabel("Número de Pasos")
axes[1].set_ylabel("Error Estándar $\sigma_{\hat{P}}$")
axes[1].set_xscale("log")
axes[1].set_yscale("log")
axes[1].legend()
axes[1].grid(True, which="both", ls="--")

plt.tight_layout()
plt.savefig('miniproyecto_1/figures/Comparacion_ds_mcmc.png')
plt.show()

# ==========================================
# 6. TABLA COMPARATIVA DE RESULTADOS
# ==========================================
df_comparacion = pd.DataFrame(
    [
        {
            "Método": "Muestreo Directo",
            "N Muestras": N_MUESTRAS,
            "Hits Totales": hits_dir,
            "Prob. Estimada": prob_dir[-1],
            "Error Estándar": error_dir[-1],
            "Tiempo Ejecución (s)": round(t_dir, 3),
            "Muestras / Seg": round(N_MUESTRAS / t_dir, 1),
        },
        {
            "Método": "MCMC Metropolis",
            "N Muestras": N_MUESTRAS,
            "Hits Totales": hits_mcmc,
            "Prob. Estimada": prob_mcmc[-1],
            "Error Estándar": error_mcmc[-1],
            "Tiempo Ejecución (s)": round(t_mcmc, 3),
            "Muestras / Seg": round(N_MUESTRAS / t_mcmc, 1),
        },
    ]
)


df_comparacion.to_csv("miniproyecto_1/data/Tabla_comparativa.csv", index=False, encoding="utf-8")


