import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Cursor, Button
import csv
from scipy.signal import find_peaks

from optic_params import Trans_Intensity

initial_ro = 0.9     # Коэффициент отражения
initial_f = 3e12     # Частота (Гц)
initial_n_real = 1.2  # Действительная часть
initial_n_imag = 0.0  # Мнимая часть (начальное значение)
initial_d = 3e-5     # Толщина плёнки (м)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, right=0.75, bottom=0.4)

trans_intensity = Trans_Intensity(
    ro=initial_ro, 
    f=initial_f, 
    n_real=initial_n_real, 
    n_imag=initial_n_imag, 
    d=initial_d
)


# Диапазон значений Δ
delta_values = np.linspace(1e-4, 1e-3, 100000)

line, = ax.plot(delta_values*1e3, trans_intensity(delta_values))

ax.set_title('Зависимость интенсивности от Δ')
ax.set_xlabel('Δ, мм')
ax.set_ylabel('Относительная Интенсивность')
ax.grid(True)

cursor = Cursor(ax, horizOn=True, vertOn=True, color='r', lw=1)


ax_freq = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_n_real = plt.axes([0.2, 0.20, 0.65, 0.03])
ax_n_imag = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_d = plt.axes([0.2, 0.10, 0.65, 0.03])
ax_ro = plt.axes([0.2, 0.05, 0.65, 0.03])

ax_print = plt.axes([0.85, 0.6, 0.05, 0.05])

slider_f = Slider(
    ax=ax_freq,
    label='Частота (ТГц)',
    valmin=1,
    valmax=10,
    valinit=initial_f * (10 ** -12),
    valstep=0.01
)

slider_n_real = Slider(
    ax=ax_n_real,
    label='Re(n)',
    valmin=1.0,
    valmax=3.0,
    valinit=initial_f * (10 ** -12),
    valstep=0.01
)

slider_n_imag = Slider(
    ax=ax_n_imag,
    label='Im(n)',
    valmin=0.0,
    valmax=1.0,
    valinit=initial_n_imag,
    valstep=0.01
)

slider_d = Slider(
    ax=ax_d,
    label='Толщина плёнки (мкм)',
    valmin=1,
    valmax=300,
    valinit=initial_d * (10 ** 6),
    valstep=1
)

slider_ro = Slider(
    ax=ax_ro,
    label='Коэффициент отражение стёкол',
    valmin=0.1,
    valmax=0.9,
    valinit=initial_ro,
    valstep=0.1
)

button_print = Button(ax_print, 'Печать')

def save_peaks(event):
    intensity = trans_intensity.get_intensity(delta_values)
    
    peaks, _ = find_peaks(intensity, height=0.5, distance=1000)
    
    peak_deltas = delta_values[peaks] * 1e3 
    
    with open('peaks.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Пиковые значения Δ (мм)"])
        for delta in peak_deltas:
            writer.writerow([delta])
    
    print(f"Записано.")


button_print.on_clicked(save_peaks)

def update(val):
    trans_intensity.f = slider_f.val * 1e12
    trans_intensity.n_real = slider_n_real.val
    trans_intensity.n_imag = slider_n_imag.val
    trans_intensity.d = slider_d.val * 1e-6
    trans_intensity.ro = slider_ro.val
    trans_intensity.R = trans_intensity.ro**2
    trans_intensity.F = 4 * trans_intensity.R / (1 - trans_intensity.R)**2
    line.set_ydata(trans_intensity(delta_values))
    fig.canvas.draw_idle()

slider_f.on_changed(update)
slider_n_real.on_changed(update)
slider_n_imag.on_changed(update)
slider_d.on_changed(update)
slider_ro.on_changed(update)

plt.show()