import math  # Importa la librería matemática necesaria para operaciones como raíz cuadrada (math.sqrt) e infinito (float('inf'))

# --- FUNCIONES AUXILIARES (PUNTOS Y PAREDES) ---

def wall_time(pos_a, vel_a, sigma):
    """Calcula el tiempo hasta que un disco choque contra una pared en un solo eje (1D)."""
    if vel_a > 0.0:
        # Si la velocidad es positiva, el disco avanza hacia la pared derecha/superior (1.0 - sigma)[cite: 6]
        del_t = (1.0 - sigma - pos_a) / vel_a
    elif vel_a < 0.0:
        # Si la velocidad es negativa, el disco avanza hacia la pared izquierda/inferior (sigma)[cite: 6]
        del_t = (pos_a - sigma) / abs(vel_a)
    else:
        # Si la velocidad es cero, el disco no chocará jamás con esta pared (tiempo infinito)[cite: 6]
        del_t = float('inf')
    return del_t  # Retorna el tiempo libre calculado antes de colisionar con la pared[cite: 6]

def pair_time(pos_a, vel_a, pos_b, vel_b, sigma):
    """Calcula el tiempo analítico hasta la colisión elástica entre dos discos (a y b) en 2D."""
    # Calcula el vector de distancia relativa entre centros: Δr = r_b - r_a[cite: 6]
    del_x = [pos_b[0] - pos_a[0], pos_b[1] - pos_a[1]]
    # Calcula la norma de la distancia al cuadrado: |Δr|^2[cite: 6]
    del_x_sq = del_x[0] ** 2 + del_x[1] ** 2
    # Calcula el vector de velocidad relativa: Δv = v_b - v_a[cite: 6]
    del_v = [vel_b[0] - vel_a[0], vel_b[1] - vel_a[1]]
    # Calcula la norma de la velocidad relativa al cuadrado: |Δv|^2[cite: 6]
    del_v_sq = del_v[0] ** 2 + del_v[1] ** 2
    # Producto escalar entre velocidad relativa y posición relativa: (Δv · Δr)[cite: 6]
    scal = del_v[0] * del_x[0] + del_v[1] * del_x[1]
    # Discriminante cuadrático de la ecuación de colisión de esferas rígidas: Υ = (Δv · Δr)^2 - |Δv|^2 * (|Δr|^2 - 4*sigma^2)[cite: 6]
    Upsilon = scal ** 2 - del_v_sq * (del_x_sq - 4.0 * sigma ** 2)
    
    # Si Υ > 0 (hay solución real de intersección) y scal < 0 (los discos se están aproximando entre sí)[cite: 6]
    if Upsilon > 0.0 and scal < 0.0:
        # Aplica la fórmula cuadrática para obtener el tiempo exacto del impacto[cite: 6]
        del_t = -(scal + math.sqrt(Upsilon)) / del_v_sq
    else:
        # Si no se cruzan o se están alejando, el tiempo de colisión es infinito[cite: 6]
        del_t = float('inf')
    return del_t  # Retorna el tiempo faltante hasta la colisión mutua[cite: 6]


# --- CONFIGURACIÓN DE PARÁMETROS DEL SISTEMA Y REFERENCIAS ---

# Definición de las 3 configuraciones geométricas de referencia (a, b, c) de 4 discos[cite: 7]
conf_a = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70, 0.70))
conf_b = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75, 0.75))
conf_c = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70, 0.70))

# Lista que agrupa las tres configuraciones de interés[cite: 7]
configurations = [conf_a, conf_b, conf_c]

# Diccionario inicializador de conteo de aciertos ("hits")[cite: 7]
hits = {conf_a: 0, conf_b: 0, conf_c: 0}

# Tolerancia/semilado del cuadrado rojo alrededor de los centros de referencia[cite: 7]
del_xy = 0.10

# Posiciones iniciales no solapadas de los 4 discos en el plano[cite: 7]
pos = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]

# Vectores de velocidad inicial para cada uno de los 4 discos en (vx, vy)[cite: 7]
vel = [[0.21, 0.12], [0.71, 0.18], [-0.23, -0.79], [0.78, 0.1177]]

# Mapeo de pares (disco_id, eje) para probar choques contra las 4 paredes (X e Y)[cite: 7]
singles = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)]

# Mapeo de combinaciones únicas de parejas de discos para probar colisiones elásticas entre ellos[cite: 7]
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

sigma = 0.10      # Radio de cada disco rígido[cite: 7]
t = 0.0           # Tiempo físico acumulado de la simulación[cite: 7]
n_events = 5000000 # Número total de eventos/colisiones a calcular en la Dinámica Molecular[cite: 7]


# --- BUCLE PRINCIPAL BASADO EN EVENTOS (EVENT-DRIVEN MOLECULAR DYNAMICS) ---

for event in range(n_events):
    # Calcula el tiempo hasta la próxima colisión contra pared para cada (disco, eje)[cite: 7]
    wall_times = [wall_time(pos[k][l], vel[k][l], sigma) for k, l in singles]
    # Calcula el tiempo hasta la próxima colisión pareada para todas las parejas de discos[cite: 7]
    pair_times = [pair_time(pos[k], vel[k], pos[l], vel[l], sigma) for k, l in pairs]
    
    # Determina cuál de todos los eventos posibles ocurrirá primero en el tiempo[cite: 7]
    next_event = min(wall_times + pair_times)
    # Guarda el tiempo previo antes de hacer los avances temporales[cite: 7]
    t_previous = t
    
    # Bucle para realizar un Muestreo Regular de posiciones en instantes enteros de tiempo entre t y el próximo evento[cite: 7]
    for inter_times in range(int(t + 1), int(t + next_event + 1)):
        # Calcula el incremento de tiempo transcurrido desde el último punto registrado[cite: 7]
        del_t = inter_times - t_previous
        # Avanza las posiciones de todos los discos por movimiento rectilíneo uniforme r = r + v * dt[cite: 7]
        for k, l in singles:
            pos[k][l] += vel[k][l] * del_t
        # Actualiza el registro de tiempo previo al tiempo del entero actual[cite: 7]
        t_previous = inter_times
        
        # Evalúa si en este instante entero de tiempo las partículas están dentro de alguna configuración de referencia[cite: 7]
        for conf in configurations:
            condition_hit = True  # Asume éxito inicialmente[cite: 7]
            for b in conf:
                # Revisa si al menos un disco del sistema 'pos' cae dentro del cuadro rojo del disco de referencia 'b'[cite: 7]
                condition_b = min(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a in pos) < del_xy
                # Producto lógico (AND): se mantendrá True solo si los N discos coinciden con las cajas de la referencia[cite: 7]
                condition_hit *= condition_b
            # Si coinciden todos los discos, registra un 'hit' para la configuración correspondiente[cite: 7]
            if condition_hit:
                hits[conf] += 1
                
    # Avanza el reloj de la simulación al tiempo exacto del evento de colisión[cite: 7]
    t += next_event
    # Intervalo de tiempo restante desde la última muestra de entero hasta el choque[cite: 7]
    del_t = t - t_previous
    # Avanza las coordenadas de los discos exactamente hasta el punto geométrico de contacto[cite: 7]
    for k, l in singles:
        pos[k][l] += vel[k][l] * del_t

    # --- ACTUALIZACIÓN DE VELOCIDADES TRAS EL IMPACTO ---

    if min(wall_times) < min(pair_times):
        # Si la colisión fue contra una pared:[cite: 7]
        # Encuentra cuál disco y qué eje sufrieron el choque con la pared[cite: 7]
        collision_disk, direction = singles[wall_times.index(next_event)]
        # Invierte la dirección del vector velocidad en ese eje de movimiento (reflejo elástico)[cite: 7]
        vel[collision_disk][direction] *= -1.0
    else:
        # Si la colisión fue entre dos discos (choque elástico 2D):[cite: 7]
        # Identifica los índices (a, b) de los dos discos involucrados en el choque[cite: 7]
        a, b = pairs[pair_times.index(next_event)]
        # Calcula el vector diferencia de posición al momento del contacto: Δr = r_b - r_a[cite: 7]
        del_x = [pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]]
        # Calcula la distancia real entre centros (|Δr|)[cite: 7]
        abs_x = math.sqrt(del_x[0] ** 2 + del_x[1] ** 2)
        # Construye el vector normal unitario a la superficie de impacto: e_perp = Δr / |Δr|[cite: 7]
        e_perp = [c / abs_x for c in del_x]
        # Calcula la velocidad relativa entre las partículas: Δv = v_b - v_a[cite: 7]
        del_v = [vel[b][0] - vel[a][0], vel[b][1] - vel[a][1]]
        # Calcula la proyección de la velocidad relativa a lo largo de la normal de impacto: (Δv · e_perp)[cite: 7]
        scal = del_v[0] * e_perp[0] + del_v[1] * e_perp[1]
        
        # Aplica las ecuaciones de conservación del momento lineal y energía cinética[cite: 7]:
        for k in range(2):
            vel[a][k] += e_perp[k] * scal  # Transfiere impulso al disco 'a' en la dirección normal[cite: 7]
            vel[b][k] -= e_perp[k] * scal  # Transfiere impulso inverso al disco 'b'[cite: 7]

# --- IMPRESIÓN FINAL DE RESULTADOS ---

for conf in configurations:
    # Imprime cada configuración de referencia junto al número de veces que fue visitada[cite: 7]
    print(conf, hits[conf])