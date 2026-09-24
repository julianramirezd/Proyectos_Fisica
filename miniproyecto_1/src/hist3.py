import math
import matplotlib.pyplot as plt

def wall_time(pos_a, vel_a, sigma):
    if vel_a > 0.0:
        return (1.0 - sigma - pos_a) / vel_a
    elif vel_a < 0.0:
        return (pos_a - sigma) / abs(vel_a)
    else:
        return float('inf')

def pair_time(pos_a, vel_a, pos_b, vel_b, sigma):
    del_x = [pos_b[0] - pos_a[0], pos_b[1] - pos_a[1]]
    del_x_sq = del_x[0] ** 2 + del_x[1] ** 2
    del_v = [vel_b[0] - vel_a[0], vel_b[1] - vel_a[1]]
    del_v_sq = del_v[0] ** 2 + del_v[1] ** 2
    scal = del_v[0] * del_x[0] + del_v[1] * del_x[1]
    Upsilon = scal ** 2 - del_v_sq * (del_x_sq - 4.0 * sigma ** 2)
    
    if Upsilon > 0.0 and scal < 0.0:
        return -(scal + math.sqrt(Upsilon)) / del_v_sq
    else:
        return float('inf')

# Parámetros iniciales
N = 4
sigma = 0.1197
pos = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
vel = [[0.21, 0.12], [0.71, 0.18], [-0.23, -0.79], [0.78, 0.1177]]

singles = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)]
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

t = 0.0
n_events = 500000
histo_data_event = []

for event in range(n_events):
    wall_times = [wall_time(pos[k][l], vel[k][l], sigma) for k, l in singles]
    pair_times = [pair_time(pos[k], vel[k], pos[l], vel[l], sigma) for k, l in pairs]
    
    next_event = min(wall_times + pair_times)
    t_previous = t
    
    # Muestreo regular a tiempos enteros
    for inter_times in range(int(t + 1), int(t + next_event + 1)):
        del_t = inter_times - t_previous
        for k, l in singles:
            pos[k][l] += vel[k][l] * del_t
        t_previous = inter_times
        
        # Guardar posiciones X en cada paso de tiempo continuo
        for k in range(N):
            histo_data_event.append(pos[k][0])
            
    # Avanzar al tiempo del choque
    t += next_event
    del_t = t - t_previous
    for k, l in singles:
        pos[k][l] += vel[k][l] * del_t

    # Colisión contra pared o par de discos
    if min(wall_times) < min(pair_times):
        collision_disk, direction = singles[wall_times.index(next_event)]
        vel[collision_disk][direction] *= -1.0
    else:
        a, b = pairs[pair_times.index(next_event)]
        del_x = [pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]]
        abs_x = math.sqrt(del_x[0] ** 2 + del_x[1] ** 2)
        e_perp = [c / abs_x for c in del_x]
        del_v = [vel[b][0] - vel[a][0], vel[b][1] - vel[a][1]]
        scal = del_v[0] * e_perp[0] + del_v[1] * e_perp[1]
        
        for k in range(2):
            vel[a][k] += e_perp[k] * scal
            vel[b][k] -= e_perp[k] * scal

# Generación del Histograma
plt.figure(figsize=(8, 5))
plt.hist(histo_data_event, bins=100, density=True, color='red', alpha=0.7)
plt.xlabel('x')
plt.ylabel('frequency')
plt.title('Event-Driven Sampling: x coordinate histogram (eta=0.18)')
plt.grid(True)
plt.savefig('miniproyecto_1/figures/event_disks_histo.png')
plt.show()