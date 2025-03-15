import numpy as np
from matplotlib.widgets import Slider, TextBox, Button
import matplotlib.pyplot as plt
import os

####################################
# Cambiare per impostare gradi cerchio dentro
gradi = [15, 45, 60, 105, 135, 165]

# Impostare su True per mostrare le linee tra i blocchi o False altrimenti
linee = False
####################################


os.chdir(os.path.dirname(os.path.abspath(__file__)))
fig, ax = plt.subplots(figsize=(6,6), dpi=100)
fase_1 = 0
fase_2 = 0

def circle(radius, center=(0,0)):
    theta = np.linspace(0, 2*np.pi, 100)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return x, y

def lines(n_lines, r, R, fase=0):
    theta = np.linspace(fase, 2*np.pi+fase, n_lines+1)
    l = []
    for i in theta:
        x = [r*np.cos(i), R*np.cos(i)]
        y = [r*np.sin(i), R*np.sin(i)]
        l.append((x,y))
    return l
    
def block(n_lines, r, R, fase=0):

    x,y = circle(r)
    ax.plot(x, y, c='firebrick')
    x,y = circle(R)
    ax.plot(x, y, c='firebrick')

    l = lines(n_lines, r, R, fase)
    for i in l:
        ax.plot(i[0], i[1], c='firebrick')
    ax.plot(l[0][0], l[0][1], c='blue')
    return

def block_2(angoli, r, R, fase=0, linee=True):

    angoli = -np.pi - np.array(angoli)*np.pi/180
    fase = fase*np.pi/180

    x,y = circle(r)
    ax.plot(x, y, c='salmon')
    x,y = circle(R)
    ax.plot(x, y, c='salmon')

    for i in angoli-fase:
        x = [r*np.cos(i), R*np.cos(i)]
        y = [r*np.sin(i), R*np.sin(i)]
        ax.plot(x, y, c='salmon')
        
        X = [r*np.cos(i+np.pi), R*np.cos(i+np.pi)]
        Y = [r*np.sin(i+np.pi), R*np.sin(i+np.pi)]
        ax.plot(X, Y, c='salmon')

        ax.text(((R-r)/2+r)*np.cos(i), ((R-r)/2+r)*np.sin(i), f'{round((-np.pi -i-fase)*180/np.pi, 1)}°', fontsize=10, color='black')

        if linee: ax.plot([R*np.cos(i+np.pi), R*np.cos(i)], [R*np.sin(i+np.pi), R*np.sin(i)], c='salmon', linestyle='--')

    ax.plot([r*np.cos(-np.pi - fase), R*np.cos(-np.pi - fase)], [r*np.sin(-np.pi - fase), R*np.sin(-np.pi - fase)], c='cyan')
    return

def draw_all(gradi, fase_1, fase_2):
    
    blocks_fase = -np.pi - (fase_1)*np.pi/180

    x,y = circle(1)
    ax.plot(x, y, c='firebrick')

    block(12, 0.9, 1, fase=blocks_fase)

    block(12*9, 0.8, 0.9, fase=blocks_fase)

    block(27, 0.7, 0.8, fase=blocks_fase)

    block(0, 0.6, 0.7, fase=blocks_fase)

    block_2(gradi, 0.5, 0.6, fase=fase_2, linee=linee)

    ax.hlines(0, -1.5, -1, color='grey', linestyle='--')
    ax.axis('off')
    ax.set_xlim(-1.01, 1.01)
    ax.set_ylim(-1.01, 1.01)


def update1(val):
    ax.cla()
    global fase_1, fase_2
    fase_1 = int(val)
    draw_all(gradi, fase_1, fase_2)

def update2(val):
    ax.cla()
    global fase_1, fase_2
    fase_2 = int(val)
    draw_all(gradi, fase_1, fase_2)

def save_image(event):
    fig.savefig('output.pdf', bbox_inches='tight',dpi=300)

if __name__ == '__main__':

    draw_all(gradi, 0, 0)
    ax.axis('off')
    ax.set_xlim(-1.01, 1.01)
    ax.set_ylim(-1.01, 1.01)

    ax_freq = fig.add_axes([0.2, 0.01, 0.1, 0.05])
    fase_1_txt = TextBox(ax_freq, 'Fase1', initial=f'{0}')
    fase_1_txt.on_text_change(update1)
    ax_freq_2 = fig.add_axes([0.6, 0.01, 0.1, 0.05])
    fase_2_txt = TextBox(ax_freq_2, 'Fase2', initial=f'{0}')
    fase_2_txt.on_text_change(update2)
    ax_save = fig.add_axes([0.4, 0.01, 0.1, 0.05])
    save_button = Button(ax_save, 'Save')
    save_button.on_clicked(save_image)
    plt.show()