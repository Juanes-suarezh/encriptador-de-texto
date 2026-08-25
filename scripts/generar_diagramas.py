#!/usr/bin/env python3
"""Genera diagramas ER de calidad académica para el documento APA."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import numpy as np

OUT = Path("/workspace/docs/figuras")
OUT.mkdir(parents=True, exist_ok=True)

GREEN = "#1B4D3E"
GREEN_FILL = "#E7F0EA"
GOLD = "#8A6A2F"
GOLD_FILL = "#F7E7C6"
NAVY = "#2C4A6E"
NAVY_FILL = "#E8EEF5"
INK = "#1A1A1A"
LINE = "#444444"


def rounded_box(ax, x, y, w, h, text, fc, ec, fontsize=8.2, bold=True):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.4,
        edgecolor=ec,
        facecolor=fc,
        zorder=3,
    )
    ax.add_patch(box)
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=INK,
        fontweight="bold" if bold else "normal",
        zorder=4,
        fontfamily="serif",
    )
    return (x, y, w, h)


def diamond(ax, x, y, w, h, text, fontsize=6.4):
    pts = np.array([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]])
    poly = Polygon(pts, closed=True, facecolor=GOLD_FILL, edgecolor=GOLD, linewidth=1.15, zorder=3)
    ax.add_patch(poly)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, color=INK, zorder=4, fontfamily="serif")
    return (x, y)


def connect(ax, a, b, label_a="1", label_b="N", color=LINE):
    x1, y1 = a
    x2, y2 = b
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-", color=color, lw=1.05, shrinkA=0, shrinkB=0),
        zorder=1,
    )
    # cardinality near ends
    dx, dy = x2 - x1, y2 - y1
    dist = (dx ** 2 + dy ** 2) ** 0.5 or 1
    ux, uy = dx / dist, dy / dist
    ax.text(x1 + ux * 0.55, y1 + uy * 0.55, label_a, fontsize=7, color=GREEN, fontweight="bold", ha="center", va="center", zorder=5, fontfamily="serif")
    ax.text(x2 - ux * 0.55, y2 - uy * 0.55, label_b, fontsize=7, color=GREEN, fontweight="bold", ha="center", va="center", zorder=5, fontfamily="serif")


def draw_chen():
    fig, ax = plt.subplots(figsize=(17.2, 11.2), dpi=220)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 16)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Layer titles
    def layer_title(x, y, text):
        ax.text(x, y, text, fontsize=9, color=GOLD, fontweight="bold", fontfamily="serif", ha="left")

    layer_title(0.3, 15.45, "Seguridad y actores")
    layer_title(0.3, 12.55, "Maestros de negocio")
    layer_title(0.3, 9.35, "Estructura tarifaria (Maestro 1.2.1)")
    layer_title(0.3, 5.85, "Proceso de automatización (Excel → CSV → cargue)")
    layer_title(0.3, 2.55, "Reforma tarifaria (Maestro 1.1.1)")

    # --- Row 1: seguridad ---
    rol = rounded_box(ax, 2.4, 14.3, 2.4, 0.7, "ROL", GREEN_FILL, GREEN)
    usuario = rounded_box(ax, 7.0, 14.3, 2.6, 0.7, "USUARIO", GREEN_FILL, GREEN)
    d_posee = diamond(ax, 4.7, 14.3, 1.5, 0.7, "posee")
    connect(ax, (rol[0] + rol[2] / 2, rol[1]), (d_posee[0] - 0.75, d_posee[1]), "1", "")
    connect(ax, (d_posee[0] + 0.75, d_posee[1]), (usuario[0] - usuario[2] / 2, usuario[1]), "", "N")

    # --- Row 2: maestros ---
    cliente = rounded_box(ax, 2.6, 11.3, 2.8, 0.72, "CLIENTE", GREEN_FILL, GREEN)
    centro = rounded_box(ax, 7.1, 11.3, 2.4, 0.72, "CENTRO", GREEN_FILL, GREEN)
    producto = rounded_box(ax, 11.4, 11.3, 2.7, 0.72, "PRODUCTO", GREEN_FILL, GREEN)
    pais = rounded_box(ax, 15.6, 11.3, 2.2, 0.72, "PAÍS", GREEN_FILL, GREEN)
    cp = rounded_box(ax, 19.6, 11.3, 3.0, 0.72, "CÓDIGO_POSTAL", GREEN_FILL, GREEN)
    zona = rounded_box(ax, 15.6, 10.15, 3.1, 0.62, "ZONA_TARIFARIA", GREEN_FILL, GREEN)
    pto = rounded_box(ax, 19.6, 10.15, 2.8, 0.62, "PUNTO_VENTA", GREEN_FILL, GREEN)

    d_tiene = diamond(ax, 4.85, 11.3, 1.45, 0.62, "tiene")
    connect(ax, (cliente[0] + cliente[2] / 2, cliente[1]), (d_tiene[0] - 0.72, d_tiene[1]), "1", "")
    connect(ax, (d_tiene[0] + 0.72, d_tiene[1]), (centro[0] - centro[2] / 2, centro[1]), "", "N")

    d_cont = diamond(ax, 17.55, 11.3, 1.55, 0.62, "contiene")
    connect(ax, (pais[0] + pais[2] / 2, pais[1]), (d_cont[0] - 0.77, d_cont[1]), "1", "")
    connect(ax, (d_cont[0] + 0.77, d_cont[1]), (cp[0] - cp[2] / 2, cp[1]), "", "N")

    # --- Row 3: tarifas ---
    tarifa = rounded_box(ax, 2.6, 8.15, 2.6, 0.7, "TARIFA", GREEN_FILL, GREEN)
    vigencia = rounded_box(ax, 7.1, 8.15, 2.6, 0.7, "VIGENCIA", GREEN_FILL, GREEN)
    baremo = rounded_box(ax, 12.0, 8.15, 2.5, 0.7, "BAREMO", GREEN_FILL, GREEN)
    detalle = rounded_box(ax, 16.6, 8.15, 3.2, 0.7, "DETALLE_BAREMO", GREEN_FILL, GREEN)
    ruta = rounded_box(ax, 21.0, 8.15, 2.3, 0.7, "RUTA", GREEN_FILL, GREEN)

    d_posee_t = diamond(ax, 2.6, 9.55, 1.45, 0.58, "posee")
    connect(ax, (cliente[0], cliente[1] - 0.36), (d_posee_t[0], d_posee_t[1] + 0.29), "1", "")
    connect(ax, (d_posee_t[0], d_posee_t[1] - 0.29), (tarifa[0], tarifa[1] + 0.35), "", "N")

    d_tiene_v = diamond(ax, 4.85, 8.15, 1.4, 0.58, "tiene")
    connect(ax, (tarifa[0] + tarifa[2] / 2, tarifa[1]), (d_tiene_v[0] - 0.7, d_tiene_v[1]), "1", "")
    connect(ax, (d_tiene_v[0] + 0.7, d_tiene_v[1]), (vigencia[0] - vigencia[2] / 2, vigencia[1]), "", "N")

    d_define = diamond(ax, 9.55, 8.15, 1.5, 0.58, "define")
    connect(ax, (vigencia[0] + vigencia[2] / 2, vigencia[1]), (d_define[0] - 0.75, d_define[1]), "1", "")
    connect(ax, (d_define[0] + 0.75, d_define[1]), (baremo[0] - baremo[2] / 2, baremo[1]), "", "N")

    d_desg = diamond(ax, 14.25, 8.15, 1.55, 0.58, "desglosa")
    connect(ax, (baremo[0] + baremo[2] / 2, baremo[1]), (d_desg[0] - 0.77, d_desg[1]), "1", "")
    connect(ax, (d_desg[0] + 0.77, d_desg[1]), (detalle[0] - detalle[2] / 2, detalle[1]), "", "N")

    d_cubre = diamond(ax, 9.55, 7.05, 1.4, 0.55, "cubre")
    connect(ax, (vigencia[0] + 0.6, vigencia[1] - 0.35), (d_cubre[0] - 0.4, d_cubre[1] + 0.2), "1", "")
    connect(ax, (d_cubre[0] + 0.55, d_cubre[1] + 0.05), (ruta[0] - 0.9, ruta[1] - 0.35), "", "N")

    d_aplica = diamond(ax, 16.6, 7.05, 1.55, 0.55, "aplica en")
    connect(ax, (baremo[0] + 0.7, baremo[1] - 0.35), (d_aplica[0] - 0.6, d_aplica[1] + 0.15), "1", "")
    connect(ax, (d_aplica[0] + 0.7, d_aplica[1] + 0.1), (ruta[0] - 0.3, ruta[1] - 0.35), "", "N")

    d_usa = diamond(ax, 11.4, 9.55, 1.35, 0.55, "usa")
    connect(ax, (producto[0], producto[1] - 0.36), (d_usa[0], d_usa[1] + 0.27), "1", "")
    connect(ax, (d_usa[0] + 0.3, d_usa[1] - 0.27), (ruta[0] - 1.0, ruta[1] + 0.35), "", "N")
    connect(ax, (d_usa[0] - 0.2, d_usa[1] - 0.27), (baremo[0], baremo[1] + 0.35), "", "N")

    d_orig = diamond(ax, 21.0, 10.15, 1.45, 0.55, "ubica")
    connect(ax, (pais[0] + 1.0, pais[1] - 0.36), (d_orig[0] - 0.4, d_orig[1] + 0.2), "1", "")
    connect(ax, (cp[0], cp[1] - 0.36), (d_orig[0] + 0.2, d_orig[1] + 0.27), "1", "")
    connect(ax, (d_orig[0], d_orig[1] - 0.27), (ruta[0], ruta[1] + 0.35), "", "N")

    d_asig = diamond(ax, 7.1, 9.55, 1.4, 0.55, "asigna")
    connect(ax, (producto[0] - 1.1, producto[1] - 0.2), (d_asig[0] + 0.7, d_asig[1] + 0.1), "1", "")
    connect(ax, (d_asig[0], d_asig[1] - 0.27), (baremo[0] - 1.5, baremo[1] + 0.35), "", "N")

    # --- Row 4: proceso ---
    solicitud = rounded_box(ax, 3.0, 4.55, 2.8, 0.7, "SOLICITUD", NAVY_FILL, NAVY, fontsize=8)
    archivo = rounded_box(ax, 7.6, 4.55, 3.15, 0.7, "ARCHIVO_INSUMO", NAVY_FILL, NAVY, fontsize=8)
    fichero = rounded_box(ax, 12.5, 4.55, 2.8, 0.7, "FICHERO_CSV", NAVY_FILL, NAVY, fontsize=8)
    regla = rounded_box(ax, 17.2, 4.55, 3.2, 0.7, "REGLA_VALIDACIÓN", NAVY_FILL, NAVY, fontsize=7.8)
    resultado = rounded_box(ax, 21.4, 4.55, 3.3, 0.7, "RESULTADO_VALIDACIÓN", NAVY_FILL, NAVY, fontsize=7.2)
    cargue = rounded_box(ax, 12.5, 3.25, 2.6, 0.62, "CARGUE", NAVY_FILL, NAVY, fontsize=8)

    d_origina = diamond(ax, 2.6, 6.55, 1.5, 0.55, "origina")
    connect(ax, (cliente[0], cliente[1] - 0.36), (cliente[0], 6.9), "1", "")
    ax.plot([cliente[0], d_origina[0]], [6.9, d_origina[1] + 0.27], color=LINE, lw=1.05, zorder=1)
    connect(ax, (d_origina[0], d_origina[1] - 0.27), (solicitud[0], solicitud[1] + 0.35), "", "N")

    d_reg = diamond(ax, 7.0, 6.55, 1.55, 0.55, "registra")
    connect(ax, (usuario[0], usuario[1] - 0.35), (usuario[0], 6.9), "1", "")
    ax.plot([usuario[0], d_reg[0]], [6.9, d_reg[1] + 0.27], color=LINE, lw=1.05, zorder=1)
    connect(ax, (d_reg[0] - 0.5, d_reg[1] - 0.2), (solicitud[0] + 1.0, solicitud[1] + 0.35), "", "N")

    d_adj = diamond(ax, 5.3, 4.55, 1.45, 0.55, "adjunta")
    connect(ax, (solicitud[0] + solicitud[2] / 2, solicitud[1]), (d_adj[0] - 0.72, d_adj[1]), "1", "")
    connect(ax, (d_adj[0] + 0.72, d_adj[1]), (archivo[0] - archivo[2] / 2, archivo[1]), "", "N")

    d_gen = diamond(ax, 10.05, 4.55, 1.45, 0.55, "genera")
    connect(ax, (archivo[0] + archivo[2] / 2, archivo[1]), (d_gen[0] - 0.72, d_gen[1]), "", "")
    connect(ax, (solicitud[0] + 0.4, solicitud[1] - 0.35), (d_gen[0] - 0.3, d_gen[1] - 0.15), "1", "")
    connect(ax, (d_gen[0] + 0.72, d_gen[1]), (fichero[0] - fichero[2] / 2, fichero[1]), "", "N")

    d_val = diamond(ax, 15.0, 4.55, 1.5, 0.55, "se valida")
    connect(ax, (fichero[0] + fichero[2] / 2, fichero[1]), (d_val[0] - 0.75, d_val[1]), "1", "")
    connect(ax, (d_val[0] + 0.75, d_val[1]), (resultado[0] - 2.2, resultado[1]), "", "N")

    d_aplr = diamond(ax, 19.35, 4.55, 1.4, 0.55, "aplica")
    connect(ax, (regla[0] + regla[2] / 2, regla[1]), (d_aplr[0] - 0.7, d_aplr[1]), "1", "")
    connect(ax, (d_aplr[0] + 0.7, d_aplr[1]), (resultado[0] - resultado[2] / 2, resultado[1]), "", "N")

    d_carga = diamond(ax, 12.5, 3.9, 1.5, 0.5, "se carga")
    connect(ax, (fichero[0], fichero[1] - 0.35), (d_carga[0], d_carga[1] + 0.25), "1", "")
    connect(ax, (d_carga[0], d_carga[1] - 0.25), (cargue[0], cargue[1] + 0.31), "", "N")

    d_ejec = diamond(ax, 9.3, 3.25, 1.55, 0.5, "ejecuta")
    d_apr = diamond(ax, 15.7, 3.25, 1.5, 0.5, "aprueba")
    connect(ax, (d_ejec[0] + 0.77, d_ejec[1]), (cargue[0] - cargue[2] / 2, cargue[1]), "", "N")
    connect(ax, (d_apr[0] - 0.75, d_apr[1]), (cargue[0] + cargue[2] / 2, cargue[1]), "", "N")
    ax.text(9.3, 2.78, "1  USUARIO", fontsize=6.5, ha="center", color=GREEN, fontfamily="serif")
    ax.text(15.7, 2.78, "1  USUARIO", fontsize=6.5, ha="center", color=GREEN, fontfamily="serif")

    # --- Row 5: reforma ---
    desc = rounded_box(ax, 5.0, 1.35, 3.3, 0.7, "DESCUENTO_TARIFA", NAVY_FILL, NAVY, fontsize=8)
    mini = rounded_box(ax, 12.0, 1.35, 3.4, 0.7, "MÍNIMA_DESPACHO", NAVY_FILL, NAVY, fontsize=8)
    cargo = rounded_box(ax, 19.0, 1.35, 3.2, 0.7, "CARGO_MANEJO", NAVY_FILL, NAVY, fontsize=8)

    d_d = diamond(ax, 5.0, 2.15, 1.35, 0.5, "aplica")
    d_m = diamond(ax, 12.0, 2.15, 1.35, 0.5, "aplica")
    d_c = diamond(ax, 19.0, 2.15, 1.35, 0.5, "aplica")
    connect(ax, (d_d[0], d_d[1] - 0.25), (desc[0], desc[1] + 0.35), "1", "N")
    connect(ax, (d_m[0], d_m[1] - 0.25), (mini[0], mini[1] + 0.35), "1", "N")
    connect(ax, (d_c[0], d_c[1] - 0.25), (cargo[0], cargo[1] + 0.35), "1", "N")
    ax.text(5.0, 2.52, "CLIENTE / PRODUCTO / CENTRO", fontsize=6.2, ha="center", color=GREEN, fontfamily="serif")
    ax.text(12.0, 2.52, "CLIENTE / PRODUCTO / CENTRO", fontsize=6.2, ha="center", color=GREEN, fontfamily="serif")
    ax.text(19.0, 2.52, "CLIENTE / PRODUCTO / CENTRO", fontsize=6.2, ha="center", color=GREEN, fontfamily="serif")

    # legend
    rounded_box(ax, 1.55, 0.42, 2.2, 0.42, "Entidad", GREEN_FILL, GREEN, fontsize=7, bold=True)
    diamond(ax, 4.1, 0.42, 1.5, 0.5, "Relación")
    ax.text(6.5, 0.42, "Cardinalidad: 1  (uno)    N  (muchos)     Verde: maestros    Azul: proceso y reforma", fontsize=7.4, va="center", color=INK, fontfamily="serif")

    ax.set_title(
        "Diagrama entidad-relación del sistema de automatización tarifaria (notación de Chen)",
        fontsize=13,
        fontweight="bold",
        fontfamily="serif",
        color=GREEN,
        pad=8,
    )

    fig.tight_layout()
    path = OUT / "diagrama_er_chen.png"
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", path)


def entity_table(ax, x, y, title, rows, header_color=GREEN, w=2.55):
    n = len(rows) + 1
    row_h = 0.22
    h = n * row_h
    # header
    ax.add_patch(
        FancyBboxPatch(
            (x, y - h),
            w,
            h,
            boxstyle="square,pad=0",
            linewidth=0.9,
            edgecolor=header_color,
            facecolor="white",
            zorder=2,
        )
    )
    ax.add_patch(plt.Rectangle((x, y - row_h), w, row_h, facecolor=header_color, edgecolor=header_color, zorder=3))
    ax.text(x + w / 2, y - row_h / 2, title, ha="center", va="center", fontsize=7.2, color="white", fontweight="bold", fontfamily="serif", zorder=4)
    for i, row in enumerate(rows):
        yy = y - row_h * (i + 1.5)
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((x, y - row_h * (i + 2)), w, row_h, facecolor="#F4F7F4", edgecolor="none", zorder=3))
        ax.text(x + 0.08, yy, row, ha="left", va="center", fontsize=6.1, color=INK, fontfamily="serif", zorder=4)
    # border lines
    ax.plot([x, x + w, x + w, x, x], [y, y, y - h, y - h, y], color=header_color, lw=0.9, zorder=5)
    return x + w / 2, y - h, x, y, w, h  # bottom-center, and box


def crow_link(ax, x1, y1, x2, y2, one_at="start"):
    ax.plot([x1, x2], [y1, y2], color=GREEN, lw=1.0, zorder=1)


def draw_crowsfoot():
    fig, ax = plt.subplots(figsize=(18, 12.5), dpi=210)
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 18)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.set_title(
        "Modelo lógico entidad-relación (notación Crow’s Foot) — claves y atributos principales",
        fontsize=13,
        fontweight="bold",
        fontfamily="serif",
        color=GREEN,
        pad=10,
    )

    # Column 1
    c_rol = entity_table(ax, 0.3, 17.4, "ROL", ["PK  id_rol", "    nombre_rol", "    descripcion"], w=2.5)
    c_usu = entity_table(ax, 0.3, 15.35, "USUARIO", ["PK  id_usuario", "FK  id_rol", "    nombres", "    apellidos", "    correo", "    estado"], w=2.5)
    c_cli = entity_table(ax, 0.3, 12.55, "CLIENTE", ["PK  id_cliente", "UK  agrupador", "    nit_oracle", "    nombre_cliente", "    tipo_cliente B2B/B2C", "    ciudad / direccion", "    ejecutivo_cuenta", "    fecha_reforma", "    cliente_reforma", "    estado"], w=2.5)
    c_cen = entity_table(ax, 0.3, 8.55, "CENTRO", ["PK  id_centro", "FK  id_cliente", "    codigo_centro (2)", "    nombre_centro"], w=2.5)
    c_pto = entity_table(ax, 0.3, 6.35, "PUNTO_VENTA", ["PK  id_punto_venta", "UK  codigo_crr (8)", "    nombre_punto"], w=2.5)
    c_zon = entity_table(ax, 0.3, 4.35, "ZONA_TARIFARIA", ["PK  id_zona", "UK  codigo_zona (4)", "    nombre_zona"], w=2.5)

    # Column 2
    c_tar = entity_table(ax, 4.0, 17.4, "TARIFA", ["PK  id_tarifa", "FK  id_cliente", "    codigo_tarifa", "    tipo_tarifa", "    naturaleza", "    estado"], w=2.55)
    c_vig = entity_table(ax, 4.0, 14.4, "VIGENCIA", ["PK  id_vigencia", "FK  id_tarifa", "    fecha_desde", "    fecha_hasta", "    estado"], w=2.55)
    c_pro = entity_table(ax, 4.0, 11.7, "PRODUCTO", ["PK  id_producto", "UK  codigo_producto (4)", "    nombre_producto", "    tipo_producto", "    tipo_cliente", "    tipo_baremo", "    factor_volumetrico", "    moneda"], w=2.55)
    c_pai = entity_table(ax, 4.0, 8.3, "PAIS", ["PK  codigo_pais (3)", "    nombre_pais"], w=2.55)
    c_cp = entity_table(ax, 4.0, 6.55, "CODIGO_POSTAL", ["PK  id_codigo_postal", "FK  codigo_pais", "UK  codigo_postal (6)", "    ciudad"], w=2.55)

    # Column 3
    c_bar = entity_table(ax, 7.8, 17.4, "BAREMO", ["PK  id_baremo", "FK  id_vigencia", "FK  id_producto", "    numero_baremo", "    tipo_baremo", "    valor_fijo", "    valor_minimo"], w=2.6)
    c_det = entity_table(ax, 7.8, 14.15, "DETALLE_BAREMO", ["PK  id_detalle", "FK  id_baremo", "    hasta_kg", "    importe", "    sobrepeso", "    cop_unidad", "    fraccion", "    porcentaje"], w=2.6)
    c_rut = entity_table(ax, 7.8, 10.7, "RUTA", ["PK  id_ruta", "FK  id_vigencia", "FK  id_producto", "FK  id_baremo", "FK  pais_origen", "FK  id_cp_origen", "FK  pais_destino", "FK  id_cp_destino", "    conversion_vol", "    moneda", "    llave_porte"], w=2.6)

    # Column 4 proceso
    c_sol = entity_table(ax, 11.7, 17.4, "SOLICITUD", ["PK  id_solicitud", "FK  id_cliente", "FK  id_usuario_registro", "    tipo_solicitud", "    canal_recepcion", "    fecha_solicitud", "    estado", "    observaciones"], header_color=GOLD, w=2.85)
    c_arc = entity_table(ax, 11.7, 13.85, "ARCHIVO_INSUMO", ["PK  id_archivo", "FK  id_solicitud", "    nombre_archivo", "    tipo_insumo", "    ruta_almacenamiento", "    fecha_carga", "    hash_integridad"], header_color=GOLD, w=2.85)
    c_fic = entity_table(ax, 11.7, 10.6, "FICHERO_CSV", ["PK  id_fichero", "FK  id_solicitud", "    tipo_fichero", "    nombre_fichero", "    separador  (|)", "    fecha_generacion", "    estado_validacion", "    ruta_archivo"], header_color=GOLD, w=2.85)
    c_car = entity_table(ax, 11.7, 7.15, "CARGUE", ["PK  id_cargue", "FK  id_fichero", "FK  id_usuario_carga", "FK  id_usuario_aprueba", "    fecha_cargue", "    medio_cargue", "    resultado", "    log_sistema", "    registro_sox"], header_color=GOLD, w=2.85)

    # Column 5 validacion + reforma
    c_reg = entity_table(ax, 15.8, 17.4, "REGLA_VALIDACION", ["PK  id_regla", "    tipo_fichero", "    nombre_campo", "    tipo_dato", "    longitud", "    obligatorio", "    expresion_regla", "    mensaje_error"], header_color=GOLD, w=3.0)
    c_res = entity_table(ax, 15.8, 13.85, "RESULTADO_VALIDACION", ["PK  id_resultado", "FK  id_fichero", "FK  id_regla", "    fila_afectada", "    resultado", "    detalle"], header_color=GOLD, w=3.0)
    c_des = entity_table(ax, 15.8, 10.8, "DESCUENTO_TARIFA", ["PK  id_descuento", "FK  id_cliente / centro", "FK  id_producto", "FK  id_punto_venta", "FK  id_zona", "    concepto_facturable", "    desde_kg / hasta_kg", "    descuento", "    fecha_desde/hasta/baja"], header_color=NAVY, w=3.0)
    c_min = entity_table(ax, 15.8, 6.85, "MINIMA_DESPACHO", ["PK  id_minima", "FK  id_cliente / centro", "FK  id_producto", "    rango_kg", "    minimo", "    baremo", "    fecha_desde/hasta/baja"], header_color=NAVY, w=3.0)
    c_cgo = entity_table(ax, 20.1, 10.8, "CARGO_MANEJO", ["PK  id_cargo", "FK  id_cliente / centro", "FK  id_producto", "    tasa_manejo", "    minimo", "    fecha_desde/hasta/baja"], header_color=NAVY, w=2.9)

    def link(a, b):
        # a, b are (cx, bottom_y, x, y, w, h)
        x1 = a[2] + a[4]
        y1 = a[3] - a[5] / 2
        x2 = b[2]
        y2 = b[3] - b[5] / 2
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.05, mutation_scale=8),
            zorder=1,
        )

    # key relationships (left to right flow)
    link(c_rol, c_usu)
    link(c_cli, c_tar)
    link(c_tar, c_vig)
    link(c_vig, c_bar)
    link(c_bar, c_det)
    link(c_pro, c_bar)
    link(c_vig, c_rut)
    link(c_bar, c_rut)
    link(c_pro, c_rut)
    link(c_pai, c_cp)
    link(c_cli, c_sol)
    link(c_usu, c_sol)
    link(c_sol, c_arc)
    link(c_sol, c_fic)
    link(c_fic, c_car)
    link(c_fic, c_res)
    link(c_reg, c_res)
    link(c_cli, c_des)
    link(c_cli, c_min)
    link(c_pro, c_des)

    ax.text(
        13.0,
        0.45,
        "PK = llave primaria    FK = llave foránea    UK = llave única    →  relación 1:N (el lado de la flecha es el lado N).  "
        "Verde: maestros tarifarios.  Dorado: flujo de automatización.  Azul: reforma tarifaria.",
        ha="center",
        fontsize=7.4,
        color=INK,
        fontfamily="serif",
    )

    fig.tight_layout()
    path = OUT / "diagrama_er_crowsfoot.png"
    fig.savefig(path, dpi=210, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", path)


if __name__ == "__main__":
    draw_chen()
    draw_crowsfoot()
