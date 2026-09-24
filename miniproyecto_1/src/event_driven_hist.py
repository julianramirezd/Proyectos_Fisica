import itertools
import json
import math
import matplotlib.pyplot as plt
import numpy as np

# Funciones de tiempo de colision (sin cambios)

def wall_time(pos_a, vel_a, sigma):
    if vel_a > 0.0:
        del_t = (1.0 - sigma - pos_a) / vel_a
    elif vel_a < 0.0:
        del_t = (pos_a - sigma) / abs(vel_a)
    else:
        del_t = float('inf')
    return del_t

def pair_time(pos_a, vel_a, pos_b, vel_b, sigma):
    del_x = [pos_b[0]-pos_a[0], pos_b[1]-pos_a[1]]
    del_x_sq = del_x[0]**2 + del_x[1]**2
    del_v = [vel_b[0]-vel_a[0], vel_b[1]-vel_a[1]]
    del_v_sq = del_v[0]**2 + del_v[1]**2
    scal = del_v[0]*del_x[0] + del_v[1]*del_x[1]
    Upsilon = scal**2 - del_v_sq*(del_x_sq - 4.0*sigma**2)
    if Upsilon > 0.0 and scal < 0.0:
        del_t = -(scal + math.sqrt(Upsilon))/del_v_sq
    else:
        del_t = float('inf')
    return del_t


# Configuraciones de referencia (sin cambios)

conf_a = ((0.30,0.30),(0.30,0.70),(0.70,0.30),(0.70,0.70))
conf_b = ((0.20,0.20),(0.20,0.80),(0.75,0.20),(0.75,0.75))
conf_c = ((0.30,0.20),(0.20,0.80),(0.70,0.20),(0.70,0.70))
configurations = [conf_a, conf_b, conf_c]
hits = {conf_a:0, conf_b:0, conf_c:0}
del_xy = 0.10

pos = [[0.25,0.25],[0.75,0.25],[0.25,0.75],[0.75,0.75]]
vel = [[0.21,0.12],[0.71,0.18],[-0.23,-0.79],[0.78,0.1177]]

n_particles = len(pos)
singles = [(k,l) for k in range(n_particles) for l in range(2)]
pairs = list(itertools.combinations(range(n_particles), 2))

sigma = 0.10
t = 0.0
n_events = 3_000_000

# ---------------------------------------------------------------
# 3) NUEVO para el punto 9:
#    - acumuladores de histograma para las posiciones (x,y) que el
#      programa muestrea cada vez que evalua las configuraciones.
#      En vez de guardar cada punto (esto explotaria la memoria
#      con 3 millones de eventos), se acumula directamente en un
#      histograma 2D de (n_bins x n_bins).
# ---------------------------------------------------------------
n_bins = 20
hist2d = np.zeros((n_bins, n_bins))
n_samples = 0

for event in range(n_events):
    wall_times = [wall_time(pos[k][l], vel[k][l], sigma) for k,l in singles]
    pair_times = [pair_time(pos[k], vel[k], pos[l], vel[l], sigma) for k,l in pairs]
    next_event = min(wall_times + pair_times)
    t_previous = t
    for inter_times in range(int(t+1), int(t+next_event+1)):
        delta = inter_times - t_previous
        for k,l in singles:
            pos[k][l] += vel[k][l]*delta
        t_previous = inter_times

        # --- registrar la posicion de los 4 discos en el histograma ---
        for a in pos:
            ix = min(int(a[0]*n_bins), n_bins-1)
            iy = min(int(a[1]*n_bins), n_bins-1)
            hist2d[ix, iy] += 1
        n_samples += 1

        # --- conteo de "hits" para las 3 configuraciones (igual que antes) ---
        for conf in configurations:
            hit = True
            for b in conf:
                near = min(max(abs(a[0]-b[0]), abs(a[1]-b[1])) for a in pos) < del_xy
                hit = hit and near
            if hit:
                hits[conf] += 1
    t += next_event
    delta = t - t_previous
    for k,l in singles:
        pos[k][l] += vel[k][l]*delta
    if min(wall_times) < min(pair_times):
        idx = wall_times.index(next_event)
        k,l = singles[idx]
        vel[k][l] *= -1.0
    else:
        idx = pair_times.index(next_event)
        a,b = pairs[idx]
        del_x = [pos[b][0]-pos[a][0], pos[b][1]-pos[a][1]]
        abs_x = math.sqrt(del_x[0]**2+del_x[1]**2)
        e_perp = [c/abs_x for c in del_x]
        del_v = [vel[b][0]-vel[a][0], vel[b][1]-vel[a][1]]
        scal = del_v[0]*e_perp[0] + del_v[1]*e_perp[1]
        for k in range(2):
            vel[a][k] += e_perp[k]*scal
            vel[b][k] -= e_perp[k]*scal

#for conf in configurations:
   # print(conf, hits[conf])

np.save('miniproyecto_1/data/histpos.npy', hist2d)

with open('miniproyecto_1/data/resultados_ev_N4.json','w') as f:
    json.dump({'a':hits[conf_a], 'b':hits[conf_b], 'c':hits[conf_c], 'n_samples': n_samples}, f)