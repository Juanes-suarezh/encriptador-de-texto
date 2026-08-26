#!/usr/bin/env python3
"""Genera archivos .drawio editables: DER (Chen) y MER/MR (modelo relacional)."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path("/workspace/docs/diagramas")
OUT.mkdir(parents=True, exist_ok=True)

E_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#E8F0EA;strokeColor=#1B4D3E;"
    "fontStyle=1;fontSize=12;fontFamily=Times New Roman;fontColor=#1A1A1A;"
)
E_PROC = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#E7EEF6;strokeColor=#2C4A6E;"
    "fontStyle=1;fontSize=12;fontFamily=Times New Roman;fontColor=#1A1A1A;"
)
D_STYLE = (
    "rhombus;whiteSpace=wrap;html=1;fillColor=#F7E7C6;strokeColor=#8A6A2F;"
    "fontStyle=1;fontSize=10;fontFamily=Times New Roman;fontColor=#1A1A1A;"
)
EDGE = "endArrow=none;html=1;strokeColor=#555555;strokeWidth=1.2;"
LABEL = (
    "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;"
    "fontStyle=1;fontSize=11;fontColor=#1B4D3E;fontFamily=Times New Roman;"
)
TITLE = (
    "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;"
    "fontStyle=1;fontSize=18;fontColor=#1B4D3E;fontFamily=Times New Roman;"
)
BAND = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#FAFBF9;strokeColor=#D7DED8;"
    "align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;fontStyle=1;"
    "fontSize=11;fontColor=#8A6A2F;fontFamily=Times New Roman;"
)

SWIM = (
    "swimlane;fontStyle=1;childLayout=stackLayout;horizontal=1;startSize=28;"
    "horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;"
    "collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;"
    "fillColor={fill};strokeColor={stroke};fontColor=#FFFFFF;fontSize=12;"
    "fontFamily=Times New Roman;"
)
ROW = (
    "text;strokeColor=none;fillColor={bg};align=left;verticalAlign=middle;"
    "spacingLeft=8;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];"
    "portConstraint=eastwest;whiteSpace=wrap;html=1;fontSize=10;"
    "fontFamily=Times New Roman;fontColor=#1A1A1A;{extra}"
)
REL_EDGE = (
    "html=1;strokeColor=#1B4D3E;strokeWidth=1.2;"
    "startArrow=ERone;startFill=0;endArrow=ERmany;endFill=0;"
)


def cell(cid, value, style, x, y, w, h, parent="1"):
    return (
        f'        <mxCell id="{escape(cid)}" value="{escape(value)}" style="{style}" '
        f'vertex="1" parent="{parent}">\n'
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def edge(cid, source, target, value=""):
    val = f' value="{escape(value)}"' if value else ""
    return (
        f'        <mxCell id="{escape(cid)}"{val} style="{EDGE}" edge="1" parent="1" '
        f'source="{escape(source)}" target="{escape(target)}">\n'
        f'          <mxGeometry relative="1" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def wrap(name, diagram_id, width, height, body):
    return f"""<mxfile host="app.diagrams.net" modified="2026-08-25T22:00:00.000Z" agent="Cursor" version="22.1.0" type="device">
  <diagram id="{diagram_id}" name="{escape(name)}">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{body}      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def build_der():
    b = []
    b.append(cell("title", "DER — Automatización del cargue tarifario (notación de Chen)", TITLE, 200, 12, 1400, 36))
    b.append(cell("leg", "Rectángulo = entidad    Rombo = relación    1 / N = cardinalidad    Verde = maestros    Azul = proceso y reforma", LABEL, 200, 48, 1400, 24))

    # bands
    b.append(cell("band1", "1. Seguridad y actores", BAND, 40, 80, 1920, 110))
    b.append(cell("band2", "2. Maestros de negocio", BAND, 40, 210, 1920, 150))
    b.append(cell("band3", "3. Estructura tarifaria (maestro 1.2.1)", BAND, 40, 380, 1920, 200))
    b.append(cell("band4", "4. Proceso de automatización Excel → CSV → cargue", BAND, 40, 600, 1920, 230))
    b.append(cell("band5", "5. Reforma tarifaria (maestro 1.1.1)", BAND, 40, 850, 1920, 140))

    # row 1
    b.append(cell("ROL", "ROL", E_STYLE, 620, 115, 140, 48))
    b.append(cell("d_posee", "posee", D_STYLE, 800, 112, 110, 54))
    b.append(cell("USUARIO", "USUARIO", E_STYLE, 950, 115, 150, 48))
    b.append(cell("c1", "1", LABEL, 770, 100, 20, 18))
    b.append(cell("c1n", "N", LABEL, 920, 100, 20, 18))
    b.append(edge("e_rol", "ROL", "d_posee"))
    b.append(edge("e_usu", "d_posee", "USUARIO"))

    # row 2 maestros
    maestros = [
        ("CLIENTE", 70, 270, E_STYLE),
        ("CENTRO", 340, 270, E_STYLE),
        ("PRODUCTO", 580, 270, E_STYLE),
        ("PAÍS", 840, 270, E_STYLE),
        ("CÓDIGO_POSTAL", 1100, 270, E_STYLE),
        ("ZONA_TARIFARIA", 1400, 250, E_STYLE),
        ("PUNTO_VENTA", 1400, 310, E_STYLE),
    ]
    for name, x, y, st in maestros:
        w = 170 if name not in ("CÓDIGO_POSTAL", "ZONA_TARIFARIA") else 190
        b.append(cell(name, name, st, x, y, w, 46))

    b.append(cell("d_tiene", "tiene", D_STYLE, 230, 266, 100, 52))
    b.append(cell("d_cont", "contiene", D_STYLE, 990, 266, 100, 52))
    b.append(edge("e_cli_d", "CLIENTE", "d_tiene"))
    b.append(edge("e_d_cen", "d_tiene", "CENTRO"))
    b.append(edge("e_pa_d", "PAÍS", "d_cont"))
    b.append(edge("e_d_cp", "d_cont", "CÓDIGO_POSTAL"))
    b.append(cell("c2", "1", LABEL, 210, 250, 20, 18))
    b.append(cell("c2n", "N", LABEL, 340, 250, 20, 18))
    b.append(cell("c3", "1", LABEL, 970, 250, 20, 18))
    b.append(cell("c3n", "N", LABEL, 1100, 250, 20, 18))

    # row 3 tarifas
    tarifas = [
        ("TARIFA", 70, 470),
        ("VIGENCIA", 370, 470),
        ("BAREMO", 680, 470),
        ("DETALLE_BAREMO", 1000, 470),
        ("RUTA", 1360, 470),
    ]
    for name, x, y in tarifas:
        w = 180 if name == "DETALLE_BAREMO" else 160
        b.append(cell(name, name, E_STYLE, x, y, w, 48))

    b.append(cell("d_posee_t", "posee", D_STYLE, 90, 400, 100, 50))
    b.append(cell("d_tiene_v", "tiene", D_STYLE, 250, 466, 100, 52))
    b.append(cell("d_define", "define", D_STYLE, 550, 466, 100, 52))
    b.append(cell("d_desg", "desglosa", D_STYLE, 870, 466, 110, 52))
    b.append(cell("d_cubre", "cubre", D_STYLE, 500, 540, 100, 50))
    b.append(cell("d_aplica", "aplica en", D_STYLE, 860, 540, 120, 50))
    b.append(cell("d_usa", "usa", D_STYLE, 600, 400, 90, 50))
    b.append(cell("d_ubica", "ubica", D_STYLE, 1360, 400, 100, 50))

    b.append(edge("e_cli_tar", "CLIENTE", "d_posee_t"))
    b.append(edge("e_dpt_tar", "d_posee_t", "TARIFA"))
    b.append(edge("e_tar_dtv", "TARIFA", "d_tiene_v"))
    b.append(edge("e_dtv_vig", "d_tiene_v", "VIGENCIA"))
    b.append(edge("e_vig_def", "VIGENCIA", "d_define"))
    b.append(edge("e_def_bar", "d_define", "BAREMO"))
    b.append(edge("e_bar_des", "BAREMO", "d_desg"))
    b.append(edge("e_des_det", "d_desg", "DETALLE_BAREMO"))
    b.append(edge("e_vig_cub", "VIGENCIA", "d_cubre"))
    b.append(edge("e_cub_rut", "d_cubre", "RUTA"))
    b.append(edge("e_bar_apl", "BAREMO", "d_aplica"))
    b.append(edge("e_apl_rut", "d_aplica", "RUTA"))
    b.append(edge("e_pro_usa", "PRODUCTO", "d_usa"))
    b.append(edge("e_usa_bar", "d_usa", "BAREMO"))
    b.append(edge("e_usa_rut", "d_usa", "RUTA"))
    b.append(edge("e_pa_ubi", "PAÍS", "d_ubica"))
    b.append(edge("e_cp_ubi", "CÓDIGO_POSTAL", "d_ubica"))
    b.append(edge("e_ubi_rut", "d_ubica", "RUTA"))

    # row 4 proceso
    proc = [
        ("SOLICITUD", 70, 680),
        ("ARCHIVO_INSUMO", 360, 680),
        ("FICHERO_CSV", 680, 680),
        ("RESULTADO_VALIDACIÓN", 1000, 680),
        ("REGLA_VALIDACIÓN", 1400, 680),
        ("CARGUE", 680, 780),
    ]
    for name, x, y in proc:
        w = 200 if "VALIDACIÓN" in name or name == "ARCHIVO_INSUMO" else 170
        b.append(cell(name, name, E_PROC, x, y, w, 48))

    b.append(cell("d_origina", "origina", D_STYLE, 90, 620, 100, 48))
    b.append(cell("d_registra", "registra", D_STYLE, 950, 160, 110, 50))
    b.append(cell("d_adjunta", "adjunta", D_STYLE, 250, 676, 100, 52))
    b.append(cell("d_genera", "genera", D_STYLE, 560, 676, 100, 52))
    b.append(cell("d_valida", "se valida", D_STYLE, 870, 676, 110, 52))
    b.append(cell("d_aplr", "aplica", D_STYLE, 1260, 676, 100, 52))
    b.append(cell("d_carga", "se carga", D_STYLE, 700, 735, 110, 42))
    b.append(cell("d_ejecuta", "ejecuta", D_STYLE, 480, 780, 110, 48))
    b.append(cell("d_aprueba", "aprueba", D_STYLE, 900, 780, 110, 48))

    b.append(edge("e_cli_ori", "CLIENTE", "d_origina"))
    b.append(edge("e_ori_sol", "d_origina", "SOLICITUD"))
    b.append(edge("e_usu_reg", "USUARIO", "d_registra"))
    b.append(edge("e_reg_sol", "d_registra", "SOLICITUD"))
    b.append(edge("e_sol_adj", "SOLICITUD", "d_adjunta"))
    b.append(edge("e_adj_arc", "d_adjunta", "ARCHIVO_INSUMO"))
    b.append(edge("e_sol_gen", "SOLICITUD", "d_genera"))
    b.append(edge("e_gen_fic", "d_genera", "FICHERO_CSV"))
    b.append(edge("e_fic_val", "FICHERO_CSV", "d_valida"))
    b.append(edge("e_val_res", "d_valida", "RESULTADO_VALIDACIÓN"))
    b.append(edge("e_regl_apl", "REGLA_VALIDACIÓN", "d_aplr"))
    b.append(edge("e_apl_res", "d_aplr", "RESULTADO_VALIDACIÓN"))
    b.append(edge("e_fic_car", "FICHERO_CSV", "d_carga"))
    b.append(edge("e_car_cgu", "d_carga", "CARGUE"))
    b.append(edge("e_usu_eje", "USUARIO", "d_ejecuta"))
    b.append(edge("e_eje_cgu", "d_ejecuta", "CARGUE"))
    b.append(edge("e_usu_apr", "USUARIO", "d_aprueba"))
    b.append(edge("e_apr_cgu", "d_aprueba", "CARGUE"))

    # row 5 reforma
    b.append(cell("DESCUENTO_TARIFA", "DESCUENTO_TARIFA", E_PROC, 120, 910, 220, 48))
    b.append(cell("MÍNIMA_DESPACHO", "MÍNIMA_DESPACHO", E_PROC, 720, 910, 220, 48))
    b.append(cell("CARGO_MANEJO", "CARGO_MANEJO", E_PROC, 1320, 910, 220, 48))
    b.append(cell("d_ap_d", "aplica", D_STYLE, 170, 860, 100, 44))
    b.append(cell("d_ap_m", "aplica", D_STYLE, 770, 860, 100, 44))
    b.append(cell("d_ap_c", "aplica", D_STYLE, 1370, 860, 100, 44))
    b.append(edge("e_cli_dd", "CLIENTE", "d_ap_d"))
    b.append(edge("e_pro_dd", "PRODUCTO", "d_ap_d"))
    b.append(edge("e_cen_dd", "CENTRO", "d_ap_d"))
    b.append(edge("e_dd_des", "d_ap_d", "DESCUENTO_TARIFA"))
    b.append(edge("e_cli_dm", "CLIENTE", "d_ap_m"))
    b.append(edge("e_pro_dm", "PRODUCTO", "d_ap_m"))
    b.append(edge("e_cen_dm", "CENTRO", "d_ap_m"))
    b.append(edge("e_dm_min", "d_ap_m", "MÍNIMA_DESPACHO"))
    b.append(edge("e_cli_dc", "CLIENTE", "d_ap_c"))
    b.append(edge("e_pro_dc", "PRODUCTO", "d_ap_c"))
    b.append(edge("e_cen_dc", "CENTRO", "d_ap_c"))
    b.append(edge("e_dc_car", "d_ap_c", "CARGO_MANEJO"))
    b.append(edge("e_zon_des", "ZONA_TARIFARIA", "DESCUENTO_TARIFA"))
    b.append(edge("e_pto_des", "PUNTO_VENTA", "DESCUENTO_TARIFA"))

    return wrap("DER Chen", "der-chen-tarifas", 2000, 1100, "".join(b))


def table_block(prefix, title, rows, x, y, w, fill, stroke):
    """Stacked entity table. rows: list of (text, is_pk)."""
    h = 28 + 20 * len(rows)
    parts = [cell(prefix, title, SWIM.format(fill=fill, stroke=stroke), x, y, w, h)]
    for i, (text, is_pk) in enumerate(rows):
        extra = "fontStyle=4;" if is_pk else ""
        bg = "#FFF8E1" if is_pk else ("#F4F7F4" if i % 2 == 0 else "#FFFFFF")
        cid = f"{prefix}-r{i}"
        parts.append(
            f'        <mxCell id="{escape(cid)}" value="{escape(text)}" '
            f'style="{ROW.format(bg=bg, extra=extra)}" vertex="1" parent="{escape(prefix)}">\n'
            f'          <mxGeometry y="{28 + i * 20}" width="{w}" height="20" as="geometry" />\n'
            f"        </mxCell>\n"
        )
    return "".join(parts), h


def rel(cid, src, tgt):
    return (
        f'        <mxCell id="{escape(cid)}" style="{REL_EDGE}" edge="1" parent="1" '
        f'source="{escape(src)}" target="{escape(tgt)}">\n'
        f'          <mxGeometry relative="1" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def build_mer():
    b = []
    b.append(cell("title", "MER / Modelo relacional — Automatización del cargue tarifario", TITLE, 80, 10, 1600, 34))
    b.append(cell("leg", "PK subrayada    FK = llave foránea    UK = única    Flecha: 1 → N    Verde maestros    Dorado proceso    Azul reforma", LABEL, 80, 44, 1600, 22))

    green, gold, navy = "#1B4D3E", "#8A6A2F", "#3D5A80"
    tables = [
        ("ROL", 40, 80, green, [("PK  id_rol", True), ("nombre_rol  UK", False), ("descripcion", False)]),
        ("USUARIO", 40, 220, green, [("PK  id_usuario", True), ("FK  id_rol", False), ("nombres", False), ("apellidos", False), ("correo  UK", False), ("estado", False)]),
        ("CLIENTE", 40, 430, green, [("PK  id_cliente", True), ("agrupador  UK (8)", False), ("nit_oracle  UK", False), ("nombre_cliente", False), ("tipo_cliente", False), ("ciudad", False), ("direccion", False), ("ejecutivo_cuenta", False), ("fecha_reforma", False), ("cliente_reforma", False), ("estado", False)]),
        ("CENTRO", 40, 760, green, [("PK  id_centro", True), ("FK  id_cliente", False), ("codigo_centro (2)", False), ("nombre_centro", False)]),
        ("TARIFA", 280, 80, green, [("PK  id_tarifa", True), ("FK  id_cliente", False), ("codigo_tarifa", False), ("tipo_tarifa", False), ("naturaleza", False), ("estado", False)]),
        ("VIGENCIA", 280, 280, green, [("PK  id_vigencia", True), ("FK  id_tarifa", False), ("fecha_desde", False), ("fecha_hasta", False), ("estado", False)]),
        ("PRODUCTO", 280, 480, green, [("PK  id_producto", True), ("codigo_producto UK (4)", False), ("nombre_producto", False), ("tipo_producto", False), ("tipo_cliente", False), ("tipo_baremo", False), ("factor_volumetrico", False), ("moneda", False)]),
        ("PAIS", 280, 750, green, [("PK  codigo_pais (3)", True), ("nombre_pais", False)]),
        ("CODIGO_POSTAL", 280, 870, green, [("PK  id_codigo_postal", True), ("FK  codigo_pais", False), ("codigo_postal UK (6)", False), ("ciudad", False)]),
        ("BAREMO", 530, 80, green, [("PK  id_baremo", True), ("FK  id_vigencia", False), ("FK  id_producto", False), ("numero_baremo", False), ("tipo_baremo", False), ("valor_fijo", False), ("valor_minimo", False)]),
        ("DETALLE_BAREMO", 530, 300, green, [("PK  id_detalle", True), ("FK  id_baremo", False), ("hasta_kg", False), ("importe", False), ("sobrepeso", False), ("cop_unidad", False), ("fraccion", False), ("porcentaje", False)]),
        ("RUTA", 530, 550, green, [("PK  id_ruta", True), ("FK  id_vigencia", False), ("FK  id_producto", False), ("FK  id_baremo", False), ("FK  pais_origen", False), ("FK  id_cp_origen", False), ("FK  pais_destino", False), ("FK  id_cp_destino", False), ("conversion_vol", False), ("moneda", False), ("llave_porte", False)]),
        ("ZONA_TARIFARIA", 40, 920, green, [("PK  id_zona", True), ("codigo_zona UK (4)", False), ("nombre_zona", False)]),
        ("PUNTO_VENTA", 40, 1050, green, [("PK  id_punto_venta", True), ("codigo_crr UK (8)", False), ("nombre_punto", False)]),
        ("SOLICITUD", 800, 80, gold, [("PK  id_solicitud", True), ("FK  id_cliente", False), ("FK  id_usuario_registro", False), ("tipo_solicitud", False), ("canal_recepcion", False), ("fecha_solicitud", False), ("estado", False), ("observaciones", False)]),
        ("ARCHIVO_INSUMO", 800, 330, gold, [("PK  id_archivo", True), ("FK  id_solicitud", False), ("nombre_archivo", False), ("tipo_insumo", False), ("ruta_almacenamiento", False), ("fecha_carga", False), ("hash_integridad", False)]),
        ("FICHERO_CSV", 800, 560, gold, [("PK  id_fichero", True), ("FK  id_solicitud", False), ("tipo_fichero", False), ("nombre_fichero", False), ("separador", False), ("fecha_generacion", False), ("estado_validacion", False), ("ruta_archivo", False)]),
        ("CARGUE", 800, 820, gold, [("PK  id_cargue", True), ("FK  id_fichero", False), ("FK  id_usuario_carga", False), ("FK  id_usuario_aprueba", False), ("fecha_cargue", False), ("medio_cargue", False), ("resultado", False), ("log_sistema", False), ("registro_sox", False)]),
        ("REGLA_VALIDACION", 1080, 80, gold, [("PK  id_regla", True), ("tipo_fichero", False), ("nombre_campo", False), ("tipo_dato", False), ("longitud", False), ("obligatorio", False), ("expresion_regla", False), ("mensaje_error", False)]),
        ("RESULTADO_VALIDACION", 1080, 330, gold, [("PK  id_resultado", True), ("FK  id_fichero", False), ("FK  id_regla", False), ("fila_afectada", False), ("resultado", False), ("detalle", False)]),
        ("DESCUENTO_TARIFA", 1080, 560, navy, [("PK  id_descuento", True), ("FK  id_cliente", False), ("FK  id_centro", False), ("FK  id_producto", False), ("FK  id_punto_venta", False), ("FK  id_zona", False), ("concepto_facturable", False), ("desde_kg", False), ("hasta_kg", False), ("descuento", False), ("fecha_desde", False), ("fecha_hasta", False), ("fecha_baja", False)]),
        ("MINIMA_DESPACHO", 1360, 560, navy, [("PK  id_minima", True), ("FK  id_cliente", False), ("FK  id_centro", False), ("FK  id_producto", False), ("rango_kg", False), ("minimo", False), ("baremo", False), ("fecha_desde", False), ("fecha_hasta", False), ("fecha_baja", False)]),
        ("CARGO_MANEJO", 1360, 860, navy, [("PK  id_cargo", True), ("FK  id_cliente", False), ("FK  id_centro", False), ("FK  id_producto", False), ("tasa_manejo", False), ("minimo", False), ("fecha_desde", False), ("fecha_hasta", False), ("fecha_baja", False)]),
    ]

    for name, x, y, color, rows in tables:
        xml, _ = table_block(name, name, rows, x, y, 220 if name not in ("DESCUENTO_TARIFA", "RESULTADO_VALIDACION", "REGLA_VALIDACION") else 240, color, color)
        b.append(xml)

    links = [
        ("l1", "ROL", "USUARIO"),
        ("l2", "CLIENTE", "CENTRO"),
        ("l3", "CLIENTE", "TARIFA"),
        ("l4", "TARIFA", "VIGENCIA"),
        ("l5", "VIGENCIA", "BAREMO"),
        ("l6", "VIGENCIA", "RUTA"),
        ("l7", "PRODUCTO", "BAREMO"),
        ("l8", "PRODUCTO", "RUTA"),
        ("l9", "BAREMO", "DETALLE_BAREMO"),
        ("l10", "BAREMO", "RUTA"),
        ("l11", "PAIS", "CODIGO_POSTAL"),
        ("l12", "USUARIO", "SOLICITUD"),
        ("l13", "CLIENTE", "SOLICITUD"),
        ("l14", "SOLICITUD", "ARCHIVO_INSUMO"),
        ("l15", "SOLICITUD", "FICHERO_CSV"),
        ("l16", "FICHERO_CSV", "CARGUE"),
        ("l17", "FICHERO_CSV", "RESULTADO_VALIDACION"),
        ("l18", "REGLA_VALIDACION", "RESULTADO_VALIDACION"),
        ("l19", "CLIENTE", "DESCUENTO_TARIFA"),
        ("l20", "CLIENTE", "MINIMA_DESPACHO"),
        ("l21", "CLIENTE", "CARGO_MANEJO"),
        ("l22", "PRODUCTO", "DESCUENTO_TARIFA"),
        ("l23", "CENTRO", "DESCUENTO_TARIFA"),
        ("l24", "ZONA_TARIFARIA", "DESCUENTO_TARIFA"),
        ("l25", "PUNTO_VENTA", "DESCUENTO_TARIFA"),
        ("l26", "PAIS", "RUTA"),
        ("l27", "CODIGO_POSTAL", "RUTA"),
    ]
    for cid, s, t in links:
        b.append(rel(cid, s, t))

    return wrap("MER Modelo relacional", "mer-mr-tarifas", 1700, 1280, "".join(b))


def main():
    der = OUT / "DER_parametrizacion_tarifaria.drawio"
    mer = OUT / "MER_modelo_relacional.drawio"
    der.write_text(build_der(), encoding="utf-8")
    mer.write_text(build_mer(), encoding="utf-8")
    print("saved", der)
    print("saved", mer)


if __name__ == "__main__":
    main()
