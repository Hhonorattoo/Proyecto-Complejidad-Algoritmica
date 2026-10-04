import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def graficar_potencias_diez():
    x = np.linspace(1, 10, 400)
    y_fact = np.array([math.gamma(v + 1) for v in x])
    y_hk = (x**2) * (2**x)

    c_fact, c_hk = "#E4572E", "#2E86AB"

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8))
    fig.suptitle(
        r"Complejidad: $O(n!)$ vs $O(n^2 \cdot 2^n)$",
        fontsize=16,
        fontweight="bold",
    )

    for ax in (ax1, ax2):
        ax.plot(x, y_fact, color=c_fact, lw=3, label=r"$n!$ (Fuerza bruta)")
        ax.plot(x, y_hk, color=c_hk, lw=3, label=r"$n^2 \cdot 2^n$ (Held-Karp)")
        ax.fill_between(x, y_fact, y_hk, where=y_fact > y_hk,
                        color=c_fact, alpha=0.08)
        ax.set_xlim(1, 10)
        ax.set_xticks(range(1, 11))
        ax.set_xlabel("Número de productos intermedios ($n$)", fontsize=11)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=10)
        ax.legend(fontsize=11, frameon=True, loc="upper left")

    # Escala lineal: se aprecia la explosión del factorial
    ax1.set_title("Escala lineal (se ve la diferencia real)", fontsize=12)
    ax1.set_ylim(0, 4e6)
    ax1.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda v, _: f"{v / 1e6:.1f} M")
    )
    ax1.set_ylabel("Operaciones (millones)", fontsize=11)

    # Escala logarítmica: se ve el orden de magnitud
    ax2.set_title("Escala logarítmica (órdenes de magnitud)", fontsize=12)
    ax2.set_yscale("log")
    ax2.set_ylim(1, 1e7)
    ax2.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=8))
    ax2.set_ylabel("Operaciones (log)", fontsize=11)

    plt.tight_layout()
    plt.show()


graficar_potencias_diez()