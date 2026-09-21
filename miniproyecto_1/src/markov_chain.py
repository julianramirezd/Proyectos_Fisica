"""
Módulo de Cadenas de Markov (Markov Chain)
======================================================
Simulación de N discos rígidos en un espacio bidimensional continuo (caja 1x1)
sin solapamiento, con estimación de probabilidades para configuraciones de referencia.
"""

import random
import pandas as pd

N = 4  # Número de discos rígidos (Cambiar a 8 para la segunda parte del punto 5)
sigma = 0.15  # Radio físico de los discos
sigma_sq = sigma**2  # Radio al cuadrado
delta = 0.1  # Amplitud del desplazamiento aleatorio por paso (Paso Metropolis)
del_xy = 0.05  # Tolerancia espacial de las cajas rojas
n_steps = int(1e4)  # Pasos de la cadena de Markov
num_intentos = 3  # Número de repeticiones independientes

# Configuraciones de referencia para verificar equiprobabilidad
conf_a = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70, 0.70))
conf_b = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75, 0.75))
conf_c = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70, 0.70))

configurations = [conf_a, conf_b, conf_c]

# Mapeo de nombres limpios a las tuplas de referencia (Para la generacion de .csv)
nombres_config = {
    conf_a: "Configuración A",
    conf_b: "Configuración B",
    conf_c: "Configuración C",
}

# Estructura acumuladora de todos los intentos
datos_resultados = []

for intento in range(1, num_intentos + 1):
     # Posición inicial sin solapamiento para los 4 discos en el intento actual
    L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]

    # Reiniciar el contador de aciertos (hits) para este intento
    hits = {conf_a: 0, conf_b: 0, conf_c: 0}
    
    # Evolución del sistema mediante Cadenas de Markov
    for steps in range(n_steps):
        a = random.choice(L) # Selecciona un disco aleatorio 'a' de la lista L
        b = [ a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]# Propone un desplazamiento aleatorio 'b' para el disco seleccionado dentro del rango [-delta, delta]
        # Calcula la distancia al cuadrado mínima entre la propuesta 'b' y los demás discos 'c' en L
        min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
        # Verifica las condiciones de frontera de la caja de lado 1
        box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
        # Criterio de aceptación/rechazo: Si no toca paredes ni se solapa con otros discos
        if not (box_cond or min_dist < 4.0 * sigma_sq):
            # Acepta el movimiento actualizando las coordenadas de 'a'
            a[:] = b

        # LÍNEAS INCORPORADAS DEL PROGRAMA ANTERIOR PARA VERIFICAR EQUIPROBABILIDAD 
        # En cada paso Monte Carlo se verifica si la configuración actual L coincide con conf_a, conf_b o conf_c
        for conf in configurations:
            condition_hit = True 
            for pos_ref in conf:
                # Comprueba si al menos uno de los discos de L cae dentro de la caja roja de tolerancia de pos_ref
                condition_b = (min(max(abs(disco[0] - pos_ref[0]), abs(disco[1] - pos_ref[1]))for disco in L) < del_xy)
                condition_hit *= condition_b
            # Si los N discos están dentro de las cajas de tolerancia, se suma un hit a la configuración
            if condition_hit:
                hits[conf] += 1
    for conf in configurations:
        datos_resultados.append(
            {
                "Intento": f"Intento {intento}",
                "Configuracion": nombres_config[conf],
                "N_runs": n_steps,  # Mantiene la etiqueta N_runs para consistencia con el DataFrame previo
                "Hits": hits[conf],
                "Probabilidad_Estimada": hits[conf] / n_steps,
            }
        )

# Creación del DataFrame de Pandas
df_hits = pd.DataFrame(datos_resultados)
df_hits.to_csv("miniproyecto_1/data/resultados_mcmc_N4_1e4.csv", index=False, encoding="utf-8") #Cambiar el nombre para guardar los diferentes archivos guardados en /data
