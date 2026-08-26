#!/usr/bin/env python3
"""DER Chen completo: entidades más llenas, rombos vacíos, óvalos PK llenos y atributos vacíos."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT_DIR = Path("/workspace/docs")
OUT = OUT_DIR / "DER_parametrizacion_tarifaria.drawio"
OUT2 = OUT_DIR / "diagramas" / "DER_parametrizacion_tarifaria.drawio"

# Estilos Chen
ENT_LLENA = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#82B39A;strokeColor=#1B4D3E;strokeWidth=2;"
    "fontStyle=1;fontSize=12;fontColor=#FFFFFF;fontFamily=Times New Roman;"
)
ENT_SUAVE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#DAE8FC;strokeColor=#6C8EBF;strokeWidth=1.5;"
    "fontStyle=1;fontSize=12;fontColor=#1A1A1A;fontFamily=Times New Roman;"
)
ENT_DEBIL = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#82B39A;strokeColor=#1B4D3E;strokeWidth=4;"
    "fontStyle=1;fontSize=11;fontColor=#FFFFFF;fontFamily=Times New Roman;"
)
ROMBO = (
    "rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1.2;"
    "fontStyle=0;fontSize=11;fontFamily=Times New Roman;"
)
OVAL_PK = (
    "ellipse;whiteSpace=wrap;html=1;fillColor=#FFE599;strokeColor=#D6B656;strokeWidth=1.4;"
    "fontStyle=4;fontSize=10;fontFamily=Times New Roman;"
)
OVAL_ATTR = (
    "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;strokeWidth=1;"
    "fontStyle=0;fontSize=10;fontFamily=Times New Roman;"
)
EDGE = "endArrow=none;html=1;strokeColor=#000000;strokeWidth=1;"
EDGE_OVAL = "endArrow=none;html=1;strokeColor=#888888;strokeWidth=0.8;"
LAB = (
    "text;html=1;strokeColor=none;fillColor=none;align=center;fontStyle=1;"
    "fontSize=12;fontColor=#1B4D3E;fontFamily=Times New Roman;"
)
TITLE = (
    "text;html=1;strokeColor=none;fillColor=none;align=left;fontStyle=1;"
    "fontSize=16;fontColor=#1B4D3E;fontFamily=Times New Roman;"
)
LEG_BOX = (
    "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=8;spacingTop=6;"
    "fontSize=11;fontFamily=Times New Roman;fillColor=#FFF8E7;strokeColor=#C4A35A;"
)


def cell(cid, value, style, x, y, w, h):
    return (
        f'        <mxCell id="{escape(cid)}" value="{escape(value)}" style="{style}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def edge(cid, src, tgt, style=EDGE):
    return (
        f'        <mxCell id="{escape(cid)}" style="{style}" edge="1" parent="1" '
        f'source="{escape(src)}" target="{escape(tgt)}">\n'
        f'          <mxGeometry relative="1" as="geometry" />\n'
        f"        </mxCell>\n"
    )


def ovals(prefix, ent_id, items, x0, y0, dx=95, row=0):
    """items: list of (name, is_pk). Place in a row near the entity."""
    xml = []
    y = y0 + row * 48
    for i, (name, pk) in enumerate(items):
        oid = f"{prefix}-a{i}"
        st = OVAL_PK if pk else OVAL_ATTR
        xml.append(cell(oid, name, st, x0 + i * dx, y, 88, 38))
        xml.append(edge(f"{prefix}-e{i}", oid, ent_id, EDGE_OVAL))
    return "".join(xml)


def main():
    b = []
    b.append(cell("title", "DER (Chen) — relleno correcto y atributos en óvalos", TITLE, 40, 12, 900, 28))
    b.append(cell(
        "leyenda",
        "LEYENDA DE RELLENO (Chen)\n"
        "• Rectángulo VERDE LLENO = entidad maestra (fuerte)\n"
        "• Rectángulo AZUL MENOS LLENO = entidad de proceso\n"
        "• Rectángulo borde grueso = entidad débil (DETALLE_BAREMO)\n"
        "• Rombo BLANCO (vacío) = relación  —  el 1 y la N van en la raya, junto al rectángulo\n"
        "• Óvalo AMARILLO LLENO + subrayado = llave primaria\n"
        "• Óvalo BLANCO (vacío) = atributo simple",
        LEG_BOX, 40, 44, 520, 150,
    ))

    # ---------- Maestros (llenos) ----------
    b.append(cell("USUARIO", "USUARIO", ENT_LLENA, 720, 80, 140, 46))
    b.append(ovals("u", "USUARIO", [("id_usuario", True), ("nombres", False), ("correo", False), ("rol", False)], 620, 20))

    b.append(cell("CLIENTE", "CLIENTE", ENT_LLENA, 80, 280, 140, 46))
    b.append(ovals("cl", "CLIENTE", [("id_cliente", True), ("agrupador", False), ("nombre", False), ("tipo_cliente", False)], 20, 210))

    b.append(cell("d_tiene", "tiene", ROMBO, 260, 276, 100, 52))
    b.append(cell("CENTRO", "CENTRO", ENT_LLENA, 400, 280, 130, 46))
    b.append(ovals("ce", "CENTRO", [("id_centro", True), ("codigo_centro", False)], 380, 210))
    b.append(cell("k1", "1", LAB, 230, 258, 20, 18))
    b.append(cell("kn1", "N", LAB, 370, 258, 20, 18))
    b += [edge("e_ct", "CLIENTE", "d_tiene"), edge("e_tc", "d_tiene", "CENTRO")]

    b.append(cell("PRODUCTO", "PRODUCTO", ENT_LLENA, 620, 280, 150, 46))
    b.append(ovals("pr", "PRODUCTO", [("id_producto", True), ("codigo_producto", False), ("moneda", False)], 560, 210))

    b.append(cell("PAIS", "PAÍS", ENT_LLENA, 920, 280, 120, 46))
    b.append(ovals("pa", "PAIS", [("codigo_pais", True), ("nombre_pais", False)], 880, 210))
    b.append(cell("d_cont", "contiene", ROMBO, 1080, 276, 110, 52))
    b.append(cell("CP", "CÓDIGO_POSTAL", ENT_LLENA, 1230, 280, 160, 46))
    b.append(ovals("cp", "CP", [("id_codigo_postal", True), ("codigo_postal", False)], 1200, 210))
    b.append(cell("k2", "1", LAB, 1055, 258, 20, 18))
    b.append(cell("kn2", "N", LAB, 1205, 258, 20, 18))
    b += [edge("e_pc", "PAIS", "d_cont"), edge("e_ccp", "d_cont", "CP")]

    # ---------- Tarifas ----------
    b.append(cell("TARIFA", "TARIFA", ENT_LLENA, 80, 500, 140, 46))
    b.append(ovals("ta", "TARIFA", [("id_tarifa", True), ("codigo_tarifa", False), ("tipo_tarifa", False)], 20, 430))
    b.append(cell("d_posee", "posee", ROMBO, 80, 390, 100, 50))
    b.append(cell("k3", "1", LAB, 50, 430, 20, 18))
    b.append(cell("kn3", "N", LAB, 50, 470, 20, 18))
    b += [edge("e_clp", "CLIENTE", "d_posee"), edge("e_pt", "d_posee", "TARIFA")]

    b.append(cell("d_tv", "tiene", ROMBO, 260, 496, 100, 52))
    b.append(cell("VIGENCIA", "VIGENCIA", ENT_LLENA, 400, 500, 140, 46))
    b.append(ovals("vi", "VIGENCIA", [("id_vigencia", True), ("fecha_desde", False), ("fecha_hasta", False)], 360, 430))
    b.append(cell("k4", "1", LAB, 230, 478, 20, 18))
    b.append(cell("kn4", "N", LAB, 370, 478, 20, 18))
    b += [edge("e_tt", "TARIFA", "d_tv"), edge("e_tv", "d_tv", "VIGENCIA")]

    b.append(cell("d_def", "define", ROMBO, 580, 496, 100, 52))
    b.append(cell("BAREMO", "BAREMO", ENT_LLENA, 720, 500, 140, 46))
    b.append(ovals("ba", "BAREMO", [("id_baremo", True), ("numero_baremo", False)], 690, 430))
    b.append(cell("k5", "1", LAB, 555, 478, 20, 18))
    b.append(cell("kn5", "N", LAB, 690, 478, 20, 18))
    b += [edge("e_vd", "VIGENCIA", "d_def"), edge("e_db", "d_def", "BAREMO")]

    b.append(cell("d_usa", "usa", ROMBO, 670, 390, 90, 50))
    b.append(cell("k6", "1", LAB, 640, 370, 20, 18))
    b.append(cell("kn6", "N", LAB, 720, 450, 20, 18))
    b += [edge("e_pu", "PRODUCTO", "d_usa"), edge("e_ub", "d_usa", "BAREMO")]

    b.append(cell("d_des", "desglosa", ROMBO, 900, 496, 110, 52))
    b.append(cell("DETALLE", "DETALLE_BAREMO", ENT_DEBIL, 1050, 500, 170, 46))
    b.append(ovals("de", "DETALLE", [("id_detalle", True), ("hasta_kg", False), ("importe", False), ("sobrepeso", False)], 1000, 430))
    b.append(cell("k7", "1", LAB, 875, 478, 20, 18))
    b.append(cell("kn7", "N", LAB, 1025, 478, 20, 18))
    b += [edge("e_bd", "BAREMO", "d_des"), edge("e_dd", "d_des", "DETALLE")]

    b.append(cell("RUTA", "RUTA", ENT_LLENA, 1320, 500, 130, 46))
    b.append(ovals("ru", "RUTA", [("id_ruta", True),], 1310, 430))
    b.append(cell("d_cubre", "cubre", ROMBO, 850, 580, 100, 50))
    b.append(cell("d_aplica_r", "aplica", ROMBO, 1100, 580, 100, 50))
    b.append(cell("d_ubica", "ubica", ROMBO, 1320, 390, 100, 50))
    b.append(cell("k8", "1", LAB, 820, 560, 20, 18))
    b.append(cell("kn8", "N", LAB, 1280, 560, 20, 18))
    b.append(cell("k9", "1", LAB, 1075, 560, 20, 18))
    b.append(cell("kn9", "N", LAB, 1230, 560, 20, 18))
    b.append(cell("k10", "1", LAB, 1290, 370, 20, 18))
    b.append(cell("kn10", "N", LAB, 1380, 450, 20, 18))
    b += [
        edge("e_vc", "VIGENCIA", "d_cubre"), edge("e_cr", "d_cubre", "RUTA"),
        edge("e_ba", "BAREMO", "d_aplica_r"), edge("e_ar", "d_aplica_r", "RUTA"),
        edge("e_cpu", "CP", "d_ubica"), edge("e_ur", "d_ubica", "RUTA"),
        edge("e_pr", "PRODUCTO", "RUTA"),
    ]
    b.append(cell("k11", "1", LAB, 760, 360, 20, 18))
    b.append(cell("kn11", "N", LAB, 1280, 480, 20, 18))

    # ---------- Proceso (menos llenos) ----------
    b.append(cell("SOLICITUD", "SOLICITUD", ENT_SUAVE, 400, 720, 150, 46))
    b.append(ovals("so", "SOLICITUD", [("id_solicitud", True), ("estado", False), ("canal", False)], 350, 780, row=0))
    b.append(cell("d_reg", "registra", ROMBO, 720, 200, 110, 50))
    b.append(cell("k12", "1", LAB, 690, 180, 20, 18))
    b.append(cell("kn12", "N", LAB, 530, 700, 20, 18))
    b += [edge("e_ur", "USUARIO", "d_reg"), edge("e_rs", "d_reg", "SOLICITUD")]

    b.append(cell("d_ori", "origina", ROMBO, 80, 640, 100, 50))
    b.append(cell("k13", "1", LAB, 50, 620, 20, 18))
    b.append(cell("kn13", "N", LAB, 360, 700, 20, 18))
    b += [edge("e_co", "CLIENTE", "d_ori"), edge("e_os", "d_ori", "SOLICITUD")]

    b.append(cell("d_gen", "genera", ROMBO, 600, 716, 100, 52))
    b.append(cell("ARCHIVO", "ARCHIVO", ENT_SUAVE, 740, 720, 140, 46))
    b.append(ovals("ar", "ARCHIVO", [("id_archivo", True), ("tipo", False), ("nombre_archivo", False)], 700, 780))
    b.append(cell("k14", "1", LAB, 575, 698, 20, 18))
    b.append(cell("kn14", "N", LAB, 710, 698, 20, 18))
    b += [edge("e_sg", "SOLICITUD", "d_gen"), edge("e_ga", "d_gen", "ARCHIVO")]

    b.append(cell("d_val", "se valida", ROMBO, 920, 716, 110, 52))
    b.append(cell("VALIDACION", "VALIDACIÓN", ENT_SUAVE, 1070, 720, 150, 46))
    b.append(ovals("va", "VALIDACION", [("id_validacion", True), ("resultado", False), ("fila", False)], 1030, 780))
    b.append(cell("k15", "1", LAB, 895, 698, 20, 18))
    b.append(cell("kn15", "N", LAB, 1045, 698, 20, 18))
    b += [edge("e_av", "ARCHIVO", "d_val"), edge("e_vv", "d_val", "VALIDACION")]

    b.append(cell("REFORMA", "CONDICIÓN_REFORMA", ENT_SUAVE, 400, 900, 200, 46))
    b.append(ovals("re", "REFORMA", [("id_condicion", True), ("tipo", False), ("fecha_desde", False), ("descuento", False)], 320, 960))
    b.append(cell("d_ap", "aplica", ROMBO, 250, 896, 100, 52))
    b.append(cell("k16", "1", LAB, 220, 878, 20, 18))
    b.append(cell("kn16", "N", LAB, 370, 878, 20, 18))
    b += [edge("e_cla", "CLIENTE", "d_ap"), edge("e_cea", "CENTRO", "d_ap"),
          edge("e_pra", "PRODUCTO", "d_ap"), edge("e_apr", "d_ap", "REFORMA")]

    xml = f"""<mxfile host="app.diagrams.net" modified="2026-08-26T00:20:00.000Z" agent="Cursor" version="22.1.0" type="device">
  <diagram id="der-chen-ovalos" name="DER Chen con atributos">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{''.join(b)}      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    OUT.write_text(xml, encoding="utf-8")
    OUT2.parent.mkdir(parents=True, exist_ok=True)
    OUT2.write_text(xml, encoding="utf-8")
    print("saved", OUT)


if __name__ == "__main__":
    main()
