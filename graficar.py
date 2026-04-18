import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Cargar datos ──────────────────────────────────────────────────────────────
df = pd.read_csv("resumen.csv")
n  = df["n"].values

t_str = df["tiempo_strassen_avg"].values
t_bru = df["tiempo_bruta_avg"].values
i_str = df["instrucciones_strassen_avg"].values
i_bru = df["instrucciones_bruta_avg"].values

# ── Curvas teóricas ───────────────────────────────────────────────────────────
exp_strassen = np.log2(7)   # ≈ 2.807
f_bruta      = n**3
f_strassen   = n**exp_strassen

# ── Constante C para INSTRUCCIONES ───────────────────────────────────────────
mask_i = n >= 128
C_bruta_instr    = np.mean(i_bru[mask_i] / f_bruta[mask_i])
C_strassen_instr = np.mean(i_str[mask_i] / f_strassen[mask_i])

print("=== Constantes C para instrucciones ===")
print(f"  C_bruta    (instrucciones / n^3)     = {C_bruta_instr:.6f}")
print(f"  C_strassen (instrucciones / n^2.807) = {C_strassen_instr:.6f}")

# ── Constante C para TIEMPO (solo puntos con tiempo > 0 en ambos) ────────────
mask_t = (t_str > 0) & (t_bru > 0)
n_t    = n[mask_t]
ts_t   = t_str[mask_t]
tb_t   = t_bru[mask_t]

C_bruta_time    = np.mean(tb_t / n_t**3)
C_strassen_time = np.mean(ts_t / n_t**exp_strassen)

print("\n=== Constantes C para tiempo ===")
print(f"  C_bruta    (tiempo / n^3)             = {C_bruta_time:.2e}")
print(f"  C_strassen (tiempo / n^2.807)         = {C_strassen_time:.2e}")

# ══════════════════════════════════════════════════════════════════════════════
# GRÁFICA 1 — Instrucciones ejecutadas
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(n, i_bru, 'o-', color='#e74c3c', lw=2, ms=7, label='Fuerza Bruta (experimental)')
ax.plot(n, i_str, 's-', color='#2980b9', lw=2, ms=7, label='Strassen Híbrido (experimental)')
ax.plot(n, C_bruta_instr    * f_bruta,    '--', color='#c0392b', lw=1.5,
        label=f'$C_1 \\cdot n^3$  ($C_1={C_bruta_instr:.4f}$)')
ax.plot(n, C_strassen_instr * f_strassen, '--', color='#1a5276', lw=1.5,
        label=f'$C_2 \\cdot n^{{\\log_2 7}}$  ($C_2={C_strassen_instr:.4f}$)')

ax.set_xlabel('Tamaño de la matriz $n$', fontsize=13)
ax.set_ylabel('Instrucciones ejecutadas', fontsize=13)
ax.set_title('Instrucciones ejecutadas vs. Tamaño de la matriz', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.set_yscale('log')
ax.set_xscale('log', base=2)
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.grid(True, which='both', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('grafica_instrucciones.pdf', dpi=150, bbox_inches='tight')
plt.savefig('grafica_instrucciones.png', dpi=150, bbox_inches='tight')
print("\nGuardada: grafica_instrucciones.pdf / .png")

# ══════════════════════════════════════════════════════════════════════════════
# GRÁFICA 2 — Tiempo de ejecución (solo puntos con tiempo > 0 en ambos)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(n_t, tb_t, 'o-', color='#e74c3c', lw=2, ms=7, label='Fuerza Bruta (experimental)')
ax.plot(n_t, ts_t, 's-', color='#2980b9', lw=2, ms=7, label='Strassen Híbrido (experimental)')
ax.plot(n_t, C_bruta_time    * n_t**3,           '--', color='#c0392b', lw=1.5,
        label=f'$C_1 \\cdot n^3$  ($C_1={C_bruta_time:.2e}$)')
ax.plot(n_t, C_strassen_time * n_t**exp_strassen, '--', color='#1a5276', lw=1.5,
        label=f'$C_2 \\cdot n^{{\\log_2 7}}$  ($C_2={C_strassen_time:.2e}$)')

ax.set_xlabel('Tamaño de la matriz $n$', fontsize=13)
ax.set_ylabel('Tiempo de ejecución (segundos)', fontsize=13)
ax.set_title('Tiempo de ejecución vs. Tamaño de la matriz', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.set_yscale('log')
ax.set_xscale('log', base=2)
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.grid(True, which='both', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('grafica_tiempo.pdf', dpi=150, bbox_inches='tight')
plt.savefig('grafica_tiempo.png', dpi=150, bbox_inches='tight')
print("Guardada: grafica_tiempo.pdf / .png")

# ══════════════════════════════════════════════════════════════════════════════
# GRÁFICA 3 — Razón Bruta/Strassen
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))

# Razón instrucciones — todos los puntos
razon_instr = i_bru / i_str

# Razón tiempo — solo donde ambos > 0
razon_tiempo = tb_t / ts_t
teorica_all  = n**0.193

ax.plot(n,   razon_instr,  'o-', color='#8e44ad', lw=2, ms=7,
        label='Razón instrucciones (Bruta / Strassen)')
ax.plot(n_t, razon_tiempo, 's-', color='#27ae60', lw=2, ms=7,
        label='Razón tiempo (Bruta / Strassen)')
ax.plot(n,   teorica_all,  '--', color='gray', lw=1.5,
        label=r'Curva teórica $n^{0.193}$')
ax.axhline(y=1, color='black', linestyle=':', lw=1.2, label='Empate (razón = 1)')

ax.set_xlabel('Tamaño de la matriz $n$', fontsize=13)
ax.set_ylabel('Razón Bruta / Strassen', fontsize=13)
ax.set_title('Ventaja relativa de Strassen sobre Fuerza Bruta', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.set_xscale('log', base=2)
ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('grafica_razon.pdf', dpi=150, bbox_inches='tight')
plt.savefig('grafica_razon.png', dpi=150, bbox_inches='tight')
print("Guardada: grafica_razon.pdf / .png")

plt.show()
print("\nTodas las graficas generadas correctamente.")