from vpython import *
from math import sin, cos

# ==========================================
# Bloco 1. VARIÁVEIS INICIAIS
# ==========================================
L_inicial = 3.0
M_inicial = 1.0
W_inicial = 0.5
ANGULO_INICIAL = radians(10)
g = 9.8
L = L_inicial
dt = 0.01
tempo = 0

# ==========================================
# Bloco 2. CONFIGURAÇÃO DA CENA E GRADE
# ==========================================
scene = canvas(title='<h1>Simulador de Pêndulo Pro</h1>',
               width=800, height=600, center=vec(0, -1.5, 0), background=color.gray(0.1))

# Criando uma grade (Grid) para percepção de escala
for i in range(-5, 6):
    curve(pos=[vec(i, 2, -1), vec(i, -6, -1)],
          color=color.gray(0.2), radius=0.01)  # Verticais
    curve(pos=[vec(-5, i-1, -1), vec(5, i-1, -1)],
          color=color.gray(0.2), radius=0.01)  # Horizontais

ponto_suspensao = vec(0, 0, 0)
hhaste_fixa = box(pos=vec(0, 0, 0), size=vec(
    2.5, 0.05, 0.05), color=color.blue)

# ==========================================
# Bloco 3. OBJETOS DINÂMICOS
# ==========================================
pos_x = ponto_suspensao.x + L_inicial * sin(ANGULO_INICIAL)
pos_y = ponto_suspensao.y - L_inicial * cos(ANGULO_INICIAL)

peso = sphere(pos=vec(pos_x, pos_y, 0),
              radius=(M_inicial * 0.5)**(1/3) * 0.4,
              color=color.red, make_trail=True, trail_type="curve")

fio = cylinder(pos=ponto_suspensao, axis=peso.pos - ponto_suspensao,
               radius=0.02, color=color.white)

peso.w = W_inicial
peso.angulo = ANGULO_INICIAL

# ==========================================
# Bloco 4. GRÁFICOS DE ENERGIA
# ==========================================
#
grafico = graph(title="Energia vs Tempo", xtitle="Tempo (s)", ytitle="Energia (J)",
                width=400, height=250, align="right")
curva_cinetica = gcurve(color=color.cyan, label="Cinética")
curva_potencial = gcurve(color=color.orange, label="Potencial")

# ==========================================
# Bloco 5. INTERFACE E FUNÇÕES
# ==========================================
scene.append_to_caption('\n<b>⚙️ Ajustes e Visualização</b>\n\n')


def toggle_trail(c):
    peso.make_trail = c.checked
    if not c.checked:
        peso.clear_trail()


def ajustar_comprimento(s):
    global L
    L = s.value
    lbl_l.text = f" L: <b>{L:.1f} m</b>"


def ajustar_massa(i):
    try:
        m = float(i.text)
        peso.radius = (m * 0.5)**(1/3) * 0.4
        lbl_m.text = f" M: <b>{m:.1f} kg</b>"
    except:
        pass


# Checkbox para o rastro
checkbox(bind=toggle_trail,
         text='Exibir linha de movimento (rastro)  ', checked=True)
scene.append_to_caption('\n\n')

# Sliders
slider_l = slider(min=1.5, max=4.5, value=L_inicial, bind=ajustar_comprimento)
lbl_l = wtext(text=f" L: <b>{L_inicial:.1f} m</b>")
scene.append_to_caption('    ')

slider_w = slider(min=-2.0, max=2.0, value=W_inicial,
                  bind=lambda v: setattr(peso, 'w', v.value))
lbl_w = wtext(text=f" W inicial: <b>{W_inicial:.2f} rad/s</b>")
scene.append_to_caption('\n\nMassa (kg): ')
input_m = winput(text=str(M_inicial), bind=ajustar_massa, type='numeric')
lbl_m = wtext(text=f" M: <b>{M_inicial:.1f} kg</b>")

# ==========================================
# Bloco 6. SIMULAÇÃO
# ==========================================
while True:
    rate(100)

    # Física
    aceleracao_angular = -g * sin(peso.angulo) / L
    peso.w += aceleracao_angular * dt
    peso.angulo += peso.w * dt

    # Atualização de Posição
    peso.pos = vec(ponto_suspensao.x + L * sin(peso.angulo),
                   ponto_suspensao.y - L * cos(peso.angulo), 0)
    fio.axis = peso.pos - ponto_suspensao

    # Cálculos de Energia
    v_linear = peso.w * L
    h = L * (1 - cos(peso.angulo))
    energia_k = 0.5 * M_inicial * (v_linear**2)
    energia_p = M_inicial * g * h

    # Atualiza Gráfico
    tempo += dt
    curva_cinetica.plot(tempo, energia_k)
    curva_potencial.plot(tempo, energia_p)
