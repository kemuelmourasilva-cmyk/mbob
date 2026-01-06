# ==========================================
# BLOCO 1: IMPORTAÇÃO DE BIBLIOTECAS
# ==========================================
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from vpython import *

# ==========================================
# BLOCO 2: PARÂMETROS E CÁLCULO DA FÍSICA
# ==========================================
# Parâmetros do sistema
m = 1.0       # massa (kg)
k = 10.0      # constante da mola (N/m)
dt = 0.01     # passo de tempo (s)
t_max = 10.0  # tempo total (s)

# Condições iniciais
x0 = 1.0      # posição inicial
v0 = 0.0      # velocidade inicial

# Preparação dos arrays
t = np.arange(0, t_max, dt)
x = np.zeros_like(t)
v = np.zeros_like(t)

x[0] = x0
v[0] = v0

# Loop de Simulação (Método de Euler-Cromer)
for i in range(len(t) - 1):
    a = -k * x[i] / m            # Aceleração baseada na Lei de Hooke
    v[i+1] = v[i] + a * dt       # Atualiza velocidade
    x[i+1] = x[i] + v[i+1] * dt   # Atualiza posição

# ==========================================
# BLOCO 3: ANIMAÇÃO VISUAL 3D (VPYTHON)
# ==========================================
# Criação do cenário (abre no navegador)
scene = canvas(title='Oscilador Harmônico 3D', width=800, height=400)
parede = box(pos=vector(-1.5, 0, 0), size=vector(0.05, 0.5, 0.5), color=color.white)
massa_3d = sphere(pos=vector(x[0], 0, 0), radius=0.1, color=color.red)
mola_3d = helix(pos=parede.pos, axis=massa_3d.pos - parede.pos, radius=0.05, coils=12)

print("Iniciando animação 3D no navegador...")
for i in range(len(t)):
    rate(100) # Controla a velocidade (100 frames por segundo)
    massa_3d.pos.x = x[i]
    mola_3d.axis = massa_3d.pos - parede.pos

# ==========================================
# BLOCO 4: ANIMAÇÃO DO GRÁFICO (MATPLOTLIB)
# ==========================================
fig, ax = plt.subplots()
ax.set_xlim(0, t_max)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Gráfico da Posição em Tempo Real')
ax.set_xlabel('Tempo (s)')
ax.set_ylabel('Posição (m)')
ax.grid(True)

line, = ax.plot([], [], lw=2, color='blue')

def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data(t[:i], x[:i])
    return line,

# Criar a animação do gráfico
ani = animation.FuncAnimation(fig, animate, init_func=init, 
                               frames=len(t), interval=10, blit=True)

plt.show()