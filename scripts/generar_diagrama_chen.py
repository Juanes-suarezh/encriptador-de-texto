#!/usr/bin/env python3
"""Diagrama ER Chen limpio, por capas, para inserción en Word."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
import numpy as np

OUT = Path("/workspace/docs/figuras")
GREEN = "#1B4D3E"
GREEN_FILL = "#E8F2EB"
GOLD = "#8A6A2F"
GOLD_FILL = "#F8EBD0"
NAVY = "#2C4A6E"
NAVY_FILL = "#E7EEF6"
INK = "#1A1A1A"
LINE = "#4A4A4A"


def box(ax, x, y, text, w=2.35, h=0.62, fc=GREEN_FILL, ec=GREEN, fs=8.4):
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.015,rounding_size=0.07",
            linewidth=1.45,
            edgecolor=ec,
            facecolor=fc,
            zorder=3,
        )
    )
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, fontweight="bold",
            color=INK, zorder=4, fontfamily="serif")
    return x, y, w, h


def dia(ax, x, y, text, w=1.42, h=0.52, fs=6.5):
    pts = np.array([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]])
    ax.add_patch(Polygon(pts, closed=True, facecolor=GOLD_FILL, edgecolor=GOLD, lw=1.15, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=4, fontfamily="serif")
    return x, y, w, h


def hline(ax, x1, x2, y):
    ax.plot([x1, x2], [y, y], color=LINE, lw=1.05, zorder=1)


def vline(ax, x, y1, y2):
    ax.plot([x, x], [y1, y2], color=LINE, lw=1.05, zorder=1)


def card(ax, x, y, t):
    ax.text(x, y, t, fontsize=7.2, color=GREEN, fontweight="bold", ha="center", va="center",
            zorder=5, fontfamily="serif",
            bbox=dict(boxstyle="round,pad=0.08", fc="white", ec="none", alpha=0.92))


def band(ax, y0, y1, title):
    ax.add_patch(Rectangle((0.15, y0), 23.7, y1 - y0, facecolor="#FAFBF9", edgecolor="#D7DED8", lw=0.6, zorder=0))
    ax.text(0.28, y1 - 0.28, title, fontsize=8.2, color=GOLD, fontweight="bold", fontfamily="serif", ha="left", zorder=2)


def main():
    fig, ax = plt.subplots(figsize=(16.8, 11.4), dpi=230)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 16.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.set_title(
        "Diagrama entidad-relación del sistema de automatización tarifaria\n(notación de Chen)",
        fontsize=13.5, fontweight="bold", fontfamily="serif", color=GREEN, pad=6,
    )

    # bands
    band(ax, 13.55, 15.85, "1. Seguridad y actores")
    band(ax, 10.55, 13.35, "2. Maestros de negocio")
    band(ax, 6.85, 10.35, "3. Estructura tarifaria (maestro 1.2.1 de Alertran Padua)")
    band(ax, 3.15, 6.65, "4. Proceso de automatización (Excel → CSV → cargue)")
    band(ax, 0.55, 2.95, "5. Reforma tarifaria (maestro 1.1.1)")

    # 1. Seguridad
    r = box(ax, 8.2, 14.55, "ROL", w=2.2)
    d1 = dia(ax, 10.55, 14.55, "posee")
    u = box(ax, 13.1, 14.55, "USUARIO", w=2.4)
    hline(ax, r[0] + r[2] / 2, d1[0] - d1[2] / 2, 14.55)
    hline(ax, d1[0] + d1[2] / 2, u[0] - u[2] / 2, 14.55)
    card(ax, 9.35, 14.82, "1")
    card(ax, 11.75, 14.82, "N")

    # 2. Maestros
    c = box(ax, 2.7, 12.05, "CLIENTE", w=2.5)
    d2 = dia(ax, 4.85, 12.05, "tiene")
    ce = box(ax, 7.05, 12.05, "CENTRO", w=2.3)
    p = box(ax, 10.35, 12.05, "PRODUCTO", w=2.55)
    pa = box(ax, 13.7, 12.05, "PAÍS", w=2.15)
    d3 = dia(ax, 15.85, 12.05, "contiene")
    cp = box(ax, 18.2, 12.05, "CÓDIGO_POSTAL", w=2.85, fs=7.8)
    z = box(ax, 21.5, 12.05, "ZONA_TARIFARIA", w=2.7, fs=7.6)
    pv = box(ax, 21.5, 11.05, "PUNTO_VENTA", w=2.7, fs=7.8)

    hline(ax, c[0] + c[2] / 2, d2[0] - d2[2] / 2, 12.05)
    hline(ax, d2[0] + d2[2] / 2, ce[0] - ce[2] / 2, 12.05)
    card(ax, 3.75, 12.32, "1")
    card(ax, 5.95, 12.32, "N")
    hline(ax, pa[0] + pa[2] / 2, d3[0] - d3[2] / 2, 12.05)
    hline(ax, d3[0] + d3[2] / 2, cp[0] - cp[2] / 2, 12.05)
    card(ax, 14.75, 12.32, "1")
    card(ax, 16.95, 12.32, "N")

    # 3. Tarifas
    t = box(ax, 2.7, 8.85, "TARIFA", w=2.5)
    d4 = dia(ax, 4.85, 8.85, "tiene")
    v = box(ax, 7.15, 8.85, "VIGENCIA", w=2.45)
    d5 = dia(ax, 9.4, 8.85, "define")
    b = box(ax, 11.7, 8.85, "BAREMO", w=2.4)
    d6 = dia(ax, 14.05, 8.85, "desglosa")
    db = box(ax, 16.55, 8.85, "DETALLE_BAREMO", w=2.9, fs=7.6)
    ru = box(ax, 20.7, 8.85, "RUTA", w=2.4)

    hline(ax, t[0] + t[2] / 2, d4[0] - d4[2] / 2, 8.85)
    hline(ax, d4[0] + d4[2] / 2, v[0] - v[2] / 2, 8.85)
    card(ax, 3.75, 9.12, "1")
    card(ax, 6.0, 9.12, "N")
    hline(ax, v[0] + v[2] / 2, d5[0] - d5[2] / 2, 8.85)
    hline(ax, d5[0] + d5[2] / 2, b[0] - b[2] / 2, 8.85)
    card(ax, 8.25, 9.12, "1")
    card(ax, 10.5, 9.12, "N")
    hline(ax, b[0] + b[2] / 2, d6[0] - d6[2] / 2, 8.85)
    hline(ax, d6[0] + d6[2] / 2, db[0] - db[2] / 2, 8.85)
    card(ax, 12.85, 9.12, "1")
    card(ax, 15.25, 9.12, "N")

    # CLIENTE posee TARIFA
    d7 = dia(ax, 2.7, 10.45, "posee")
    vline(ax, 2.7, c[1] - 0.31, d7[1] + 0.26)
    vline(ax, 2.7, d7[1] - 0.26, t[1] + 0.31)
    card(ax, 3.15, 11.15, "1")
    card(ax, 3.15, 9.65, "N")

    # PRODUCTO usa BAREMO y RUTA
    d8 = dia(ax, 10.35, 10.45, "usa")
    vline(ax, 10.35, p[1] - 0.31, d8[1] + 0.26)
    vline(ax, 10.35, d8[1] - 0.26, 9.16)
    hline(ax, 10.35, 11.7, 9.16)
    vline(ax, 11.7, 9.16, b[1] + 0.31)
    card(ax, 10.75, 11.15, "1")
    card(ax, 11.15, 9.38, "N")

    # VIGENCIA cubre RUTA
    d9 = dia(ax, 7.15, 7.75, "cubre")
    vline(ax, 7.15, v[1] - 0.31, d9[1] + 0.26)
    hline(ax, 7.15, 20.7, 7.49)
    vline(ax, 20.7, 7.49, ru[1] - 0.31)
    card(ax, 6.7, 8.18, "1")
    card(ax, 20.25, 7.72, "N")

    # BAREMO aplica en RUTA
    d10 = dia(ax, 14.9, 8.15, "aplica en", w=1.55)
    hline(ax, b[0] + 0.2, d10[0] - 0.78, 8.15)
    hline(ax, d10[0] + 0.78, ru[0] - ru[2] / 2, 8.15)
    card(ax, 13.55, 8.38, "1")
    card(ax, 16.4, 8.38, "N")

    # PAIS/CP ubican RUTA
    d11 = dia(ax, 18.2, 10.45, "ubica")
    vline(ax, 18.2, cp[1] - 0.31, d11[1] + 0.26)
    vline(ax, 13.7, pa[1] - 0.31, 10.45)
    hline(ax, 13.7, 18.2 - 0.71, 10.45)
    vline(ax, 18.2, d11[1] - 0.26, ru[1] + 0.31)
    card(ax, 18.65, 11.15, "1")
    card(ax, 18.65, 9.65, "N")

    # 4. Proceso
    s = box(ax, 2.9, 5.35, "SOLICITUD", w=2.6, fc=NAVY_FILL, ec=NAVY)
    d12 = dia(ax, 5.15, 5.35, "adjunta")
    a = box(ax, 7.55, 5.35, "ARCHIVO_INSUMO", w=2.85, fs=7.6, fc=NAVY_FILL, ec=NAVY)
    d13 = dia(ax, 10.05, 5.35, "genera")
    f = box(ax, 12.6, 5.35, "FICHERO_CSV", w=2.7, fs=8, fc=NAVY_FILL, ec=NAVY)
    d14 = dia(ax, 15.15, 5.35, "se valida")
    rv = box(ax, 17.7, 5.35, "RESULTADO_VALIDACIÓN", w=3.15, fs=6.8, fc=NAVY_FILL, ec=NAVY)
    rg = box(ax, 21.55, 5.35, "REGLA_VALIDACIÓN", w=2.85, fs=7.2, fc=NAVY_FILL, ec=NAVY)
    d15 = dia(ax, 19.7, 4.55, "aplica")
    cg = box(ax, 12.6, 3.85, "CARGUE", w=2.5, fc=NAVY_FILL, ec=NAVY)
    d16 = dia(ax, 12.6, 4.58, "se carga")
    d17 = dia(ax, 9.35, 3.85, "ejecuta")
    d18 = dia(ax, 15.85, 3.85, "aprueba")

    for x1, x2, y in [
        (s[0] + s[2] / 2, d12[0] - d12[2] / 2, 5.35),
        (d12[0] + d12[2] / 2, a[0] - a[2] / 2, 5.35),
        (a[0] + a[2] / 2, d13[0] - d13[2] / 2, 5.35),
        (d13[0] + d13[2] / 2, f[0] - f[2] / 2, 5.35),
        (f[0] + f[2] / 2, d14[0] - d14[2] / 2, 5.35),
        (d14[0] + d14[2] / 2, rv[0] - rv[2] / 2, 5.35),
    ]:
        hline(ax, x1, x2, y)
    card(ax, 4.0, 5.62, "1")
    card(ax, 6.3, 5.62, "N")
    card(ax, 8.85, 5.62, "1")
    card(ax, 11.3, 5.62, "N")
    card(ax, 13.95, 5.62, "1")
    card(ax, 16.4, 5.62, "N")

    vline(ax, 19.7, rv[1] - 0.31, d15[1] + 0.26)
    hline(ax, d15[0] + 0.71, rg[0] - 0.2, 4.55)
    vline(ax, rg[0], 4.55, rg[1] - 0.31)
    card(ax, 20.7, 4.78, "1")
    card(ax, 19.25, 4.95, "N")

    vline(ax, 12.6, f[1] - 0.31, d16[1] + 0.26)
    vline(ax, 12.6, d16[1] - 0.26, cg[1] + 0.31)
    card(ax, 13.15, 4.95, "1")
    card(ax, 13.15, 4.2, "N")

    hline(ax, d17[0] + 0.71, cg[0] - cg[2] / 2, 3.85)
    hline(ax, cg[0] + cg[2] / 2, d18[0] - 0.71, 3.85)
    ax.text(9.35, 3.42, "1  USUARIO", fontsize=6.6, ha="center", color=GREEN, fontfamily="serif")
    ax.text(15.85, 3.42, "1  USUARIO", fontsize=6.6, ha="center", color=GREEN, fontfamily="serif")
    card(ax, 10.7, 4.08, "N")
    card(ax, 14.55, 4.08, "N")

    # CLIENTE origina SOLICITUD  / USUARIO registra SOLICITUD
    d19 = dia(ax, 2.9, 6.55, "origina")
    vline(ax, 2.7, t[1] - 0.31, 6.55)  # from tarifa area down? better from cliente via left
    # draw from CLIENTE down the left margin to SOLICITUD
    vline(ax, 1.15, c[1], s[1])
    hline(ax, 1.15, c[0] - c[2] / 2, c[1])
    hline(ax, 1.15, s[0] - s[2] / 2, s[1])
    ax.text(1.15, 8.6, "origina\n1 : N", fontsize=6.4, ha="center", color=GREEN, fontfamily="serif",
            fontweight="bold")

    # USUARIO registra SOLICITUD
    vline(ax, 13.1, u[1] - 0.31, 13.45)
    # skip through - use right-side note
    ax.annotate(
        "registra  1:N",
        xy=(s[0] + 0.4, s[1] + 0.31),
        xytext=(13.1, 13.7),
        fontsize=6.5,
        color=GREEN,
        fontfamily="serif",
        fontweight="bold",
        ha="center",
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9, connectionstyle="arc3,rad=0.08"),
    )

    # 5. Reforma
    ds = box(ax, 5.2, 1.55, "DESCUENTO_TARIFA", w=3.3, fs=8, fc=NAVY_FILL, ec=NAVY)
    mi = box(ax, 12.0, 1.55, "MÍNIMA_DESPACHO", w=3.3, fs=8, fc=NAVY_FILL, ec=NAVY)
    ca = box(ax, 18.8, 1.55, "CARGO_MANEJO", w=3.2, fs=8, fc=NAVY_FILL, ec=NAVY)
    d20 = dia(ax, 5.2, 2.35, "aplica")
    d21 = dia(ax, 12.0, 2.35, "aplica")
    d22 = dia(ax, 18.8, 2.35, "aplica")
    for d, e in [(d20, ds), (d21, mi), (d22, ca)]:
        vline(ax, d[0], d[1] - 0.26, e[1] + 0.31)
        card(ax, d[0] + 0.55, 2.05, "N")
    ax.text(5.2, 2.68, "CLIENTE / CENTRO / PRODUCTO   1", fontsize=6.3, ha="center", color=GREEN, fontfamily="serif")
    ax.text(12.0, 2.68, "CLIENTE / CENTRO / PRODUCTO   1", fontsize=6.3, ha="center", color=GREEN, fontfamily="serif")
    ax.text(18.8, 2.68, "CLIENTE / CENTRO / PRODUCTO   1", fontsize=6.3, ha="center", color=GREEN, fontfamily="serif")

    # legend
    box(ax, 1.7, 0.28, "Entidad", w=1.8, h=0.38, fs=7)
    dia(ax, 3.85, 0.28, "Relación", w=1.5, h=0.4, fs=6.5)
    ax.text(
        12.4, 0.28,
        "Cardinalidad:  1 = uno    N = muchos     Verde = maestros     Azul = proceso y reforma     Dorado = relación",
        ha="center", va="center", fontsize=7.5, color=INK, fontfamily="serif",
    )

    fig.tight_layout()
    path = OUT / "diagrama_er_chen.png"
    fig.savefig(path, dpi=230, bbox_inches="tight", facecolor="white")
    plt.close()
    print("saved", path)


if __name__ == "__main__":
    main()
