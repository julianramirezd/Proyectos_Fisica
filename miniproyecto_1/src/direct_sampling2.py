"""
Módulo de Muestreo Directo (Direct Sampling Monte Carlo)
======================================================
Simulación de N discos rígidos en un espacio bidimensional continuo (caja 1x1)
sin solapamiento, con estimación de probabilidades para configuraciones de referencia.
Usado para los calculos de N=8
"""
import json
import math
import os
import random
import pandas as pd


def direct_disks_box(N, sigma):
    """Genera una configuración aleatoria no solapada de N discos de radio sigma.
    Retorna una lista de N tuplas [(x1, y1), ..., (xN, yN)] con las coordenadas
    de los centros de masa dentro de la caja unitaria.
    """
    condition = False  # Bandera de control para validar el muestreo completo sin solapamientos
    
    while not condition:
        # Posiciona aleatoriamente el primer disco asegurando que no sobresalga de las paredes
        L = [(random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))]

        # Intenta ubicar secuencialmente los N-1 discos restantes
        for k in range(1, N):
            # Propone un centro de masa aleatorio para el disco k
            a = (random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))

            #Se calcula la distancia entre centros
            min_dist = min(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) for b in L)

            # La distancia entre centros debe ser >= 2*sigma para evitar solapamientos 
            if min_dist < 2.0 * sigma:
                condition = False  # Solapamiento detectado: rechaza la configuración
                break  # Abandona el intento actual y reinicia desde el primer disco
            else:
                L.append(a)  # Disco válido: se incorpora a la configuración
                condition = True  # Marca la configuración como válida si se completa exitosamente los N discos

    return L


# Parámetros Globales del Sistema y Simulaciones

sigma = 0.0848  # Radio físico de cada disco rígido (reducido para hacer mas rapido el calculo de los problemas)
del_xy = 0.05  # Semi-ancho de la caja roja de tolerancia espacial
n_runs = int(1e4)  # Número total de muestras independientes (Se modifico para los diferentes archivos )
n_intentos = 3 # Número de repeticiones por n_runs

# Configuraciones geométricas de referencia 
conf_a = tuple(direct_disks_box(8, sigma))
conf_b = tuple(direct_disks_box(8, sigma))
conf_c = tuple(direct_disks_box(8, sigma))

configurations = [conf_a, conf_b, conf_c]
configuraciones = {"conf_a": conf_a, "conf_b": conf_b, "conf_c": conf_c}

# Guardar en data/configuraciones_ref_N8.json
ruta_json = os.path.join("miniproyecto_1", "data", "configuraciones_ref_N8.json")
os.makedirs(os.path.dirname(ruta_json), exist_ok=True)

with open(ruta_json, "w", encoding="utf-8") as f:
    json.dump(configuraciones, f, indent=4)


# Mapeo de nombres limpios a las tuplas de referencia (Para la generacion de .csv)
nombres_config = {
    conf_a: "Configuración A",
    conf_b: "Configuración B",
    conf_c: "Configuración C",
}

# Estructura acumuladora de todos los intentos
datos_resultados = []

# Bucle Principal de Muestreo Directo (Monte Carlo)
for i in range(1, n_intentos + 1):
    # Contador de aciertos (Hits) por configuración
    hits = {conf_a: 0, conf_b: 0, conf_c: 0}
    for run in range(n_runs):
        # Genera una configuración válida de 4 discos no solapados
        x_vec = direct_disks_box(8, sigma)

        # Evalúa la presencia de la configuración en cada una de las referencias (a, b, c)
        for conf in configurations:
            condition_hit = True  # Bandera booleana de coincidencia

            # Verifica si existe coincidencia espacial para cada una de las cajas rojas de la referencia
            for b in conf:
                # Evalúa si al menos una partícula de x_vec cae dentro de la caja roja ubicada en 'b'
                condition_b = min(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a in x_vec) < del_xy

                # Acumula el producto booleano (Operación AND para las N partículas)
                condition_hit *= condition_b

            # Si las N partículas coinciden simultáneamente con las cajas rojas, se registra un Hit
            if condition_hit:
                hits[conf] += 1

    for conf in configurations:
        datos_resultados.append(
            {
                "Intento": f"Intento {i}",
                "Configuracion": nombres_config[conf],
                "N_runs": n_runs,
                "Hits": hits[conf],
                "Probabilidad_Estimada": hits[conf] / n_runs,
            }
        )


# Creación del DataFrame de Pandas
df_hits = pd.DataFrame(datos_resultados)
df_hits.to_csv("miniproyecto_1/data/resultados_ds_N8_1e4.csv", index=False, encoding="utf-8") #Cambiar el nombre para guardar los diferentes archivos guardados en /data

