#!/usr/bin/env python3
"""Word de la segunda actividad: solo los 4 puntos de la guía."""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

OUT = Path("/workspace/docs/Actividad2_Entidades_Llaves_DER_MR.docx")
FIG_CHEN = Path("/workspace/docs/figuras/diagrama_er_chen.png")
FIG_CROW = Path("/workspace/docs/figuras/diagrama_er_crowsfoot.png")
INK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(255, 255, 255)
HEADER_BG = "1B4D3E"


def set_run_font(run, size=12, bold=False, italic=False, color=INK, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def pf(p, align="justify", first=True, before=0, after=0):
    fmt = p.paragraph_format
    fmt.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    fmt.line_spacing = 2.0
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    p.alignment = {
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
    }[align]
    fmt.first_line_indent = Cm(1.27) if first else Cm(0)


def body(doc, text, first=True):
    p = doc.add_paragraph()
    pf(p, first=first)
    r = p.add_run(text)
    set_run_font(r)
    return p


def center(doc, text, size=12, bold=False, italic=False):
    p = doc.add_paragraph()
    pf(p, align="center", first=False)
    r = p.add_run(text)
    set_run_font(r, size=size, bold=bold, italic=italic)


def h1(doc, text):
    p = doc.add_paragraph()
    pf(p, align="center", first=False, before=12)
    r = p.add_run(text)
    set_run_font(r, bold=True)


def h2(doc, text):
    p = doc.add_paragraph()
    pf(p, align="left", first=False, before=10)
    r = p.add_run(text)
    set_run_font(r, bold=True)


def caption(doc, kind, n, title):
    p = doc.add_paragraph()
    pf(p, align="left", first=False, before=10, after=0)
    r = p.add_run(f"{kind} {n}")
    set_run_font(r, bold=(kind == "Tabla"), italic=(kind == "Figura"))
    p2 = doc.add_paragraph()
    pf(p2, align="left", first=False, before=0, after=4)
    r2 = p2.add_run(title)
    set_run_font(r2, italic=True)


def note(doc, text):
    p = doc.add_paragraph()
    pf(p, align="left", first=False, before=2, after=6)
    r = p.add_run("Nota. ")
    set_run_font(r, size=10, italic=True)
    r2 = p.add_run(text)
    set_run_font(r2, size=10)


def shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "8A8A8A")
        borders.append(el)
    tcPr.append(borders)


def cell_text(cell, text, bold=False, size=10, color=INK, fill=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Cm(0)
    r = p.add_run(text)
    set_run_font(r, size=size, bold=bold, color=color)
    if fill:
        shade(cell, fill)
    border(cell)


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    for i, h in enumerate(headers):
        cell_text(table.rows[0].cells[i], h, bold=True, color=WHITE, fill=HEADER_BG)
    for ri, row in enumerate(rows):
        fill = "F4F7F4" if ri % 2 == 0 else "FFFFFF"
        for ci, val in enumerate(row):
            cell_text(table.rows[ri + 1].cells[ci], str(val), fill=fill)
    return table


def add_page_number(paragraph):
    run = paragraph.add_run()
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    set_run_font(run, 12)


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Inches(1))
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_page_number(hp)

    center(doc, "Universidad Militar Nueva Granada", 14, bold=True)
    center(doc, "Facultad de Ingeniería", 12, bold=True)
    center(doc, "Programa de Ingeniería Informática")
    center(doc, "")
    center(
        doc,
        "Automatización del proceso de generación y cargue de tarifas al sistema de aplicación de tarifas mediante base de datos e IA",
        14,
        bold=True,
    )
    center(doc, "")
    center(doc, "Actividad 2. Modelo de datos", italic=True)
    center(doc, "Entidades, atributos, llaves, diagrama entidad-relación y modelo relacional")
    center(doc, "")
    center(doc, "Gina Paola Susatama Molineros", bold=True)
    center(doc, "Jaime Alberto Carreño Camacho", bold=True)
    center(doc, "")
    center(doc, "Asignatura: Bases de Datos I")
    center(doc, "Docente: Osiris Torres Gutiérrez")
    center(doc, "25 de agosto de 2026")

    doc.add_page_break()

    # ---------- 1 ----------
    h1(doc, "1. Identifique las entidades y sus atributos")
    body(
        doc,
        "A partir del proceso tarifario de envío de paquetes (Excel de insumos, conversión a CSV y cargue a Alertran Padua) se identificaron 23 entidades. Un objeto se tomó como entidad cuando tiene identidad propia y persiste en el tiempo; sus propiedades se registraron como atributos.",
    )

    h2(doc, "1.1 Entidades")
    caption(doc, "Tabla", 1, "Entidades del sistema de automatización tarifaria")
    add_table(
        doc,
        ["Grupo", "Entidad", "Definición"],
        [
            ["Seguridad", "ROL", "Perfil de autorización (analista, aprobador, administrador)."],
            ["Seguridad", "USUARIO", "Persona que registra, aprueba o ejecuta el cargue."],
            ["Maestro", "CLIENTE", "Cliente B2B o B2C identificado por agrupador de 8 caracteres."],
            ["Maestro", "CENTRO", "Centro de 2 caracteres asociado al agrupador."],
            ["Maestro", "PRODUCTO", "Servicio de envío (nacional, internacional o carga), código de 4 dígitos."],
            ["Maestro", "PAÍS", "Catálogo de país, código de 3 caracteres."],
            ["Maestro", "CÓDIGO_POSTAL", "Código postal de 6 dígitos o comodín (*)."],
            ["Maestro", "ZONA_TARIFARIA", "Zona de 4 caracteres usada en reforma."],
            ["Maestro", "PUNTO_VENTA", "Punto de venta o CRR de 8 caracteres."],
            ["Tarifa", "TARIFA", "Código tarifario GENERAL, ESPECIAL o REFORMA."],
            ["Tarifa", "VIGENCIA", "Periodo de aplicación de una tarifa."],
            ["Tarifa", "BAREMO", "Escala de portes (1 a 999) de una vigencia y un producto."],
            ["Tarifa", "DETALLE_BAREMO", "Rango de peso, importe y sobrepeso del baremo."],
            ["Tarifa", "RUTA", "Origen-destino ligado a un baremo, producto y vigencia."],
            ["Proceso", "SOLICITUD", "Caso recibido por correo (B2C) o Dynamo (B2B)."],
            ["Proceso", "ARCHIVO_INSUMO", "Excel, hoja tarifaria, aval o archivo plano adjunto."],
            ["Proceso", "FICHERO_CSV", "CSV generado (rutas, baremos o reforma)."],
            ["Proceso", "REGLA_VALIDACIÓN", "Lineamiento de formato, longitud y obligatoriedad."],
            ["Proceso", "RESULTADO_VALIDACIÓN", "Hallazgo de una regla sobre una fila del fichero."],
            ["Proceso", "CARGUE", "Intento de subida por FTP o importación 12.5, con control SOX."],
            ["Reforma", "DESCUENTO_TARIFA", "Descuento de reforma por cliente, centro y producto."],
            ["Reforma", "MÍNIMA_DESPACHO", "Valor mínimo de despacho de reforma."],
            ["Reforma", "CARGO_MANEJO", "Tasa e importe mínimo de cargo por manejo."],
        ],
    )
    note(doc, "Elaboración propia a partir del proceso de parametrización tarifaria.")

    h2(doc, "1.2 Atributos")
    caption(doc, "Tabla", 2, "Atributos por entidad")
    add_table(
        doc,
        ["Entidad", "Atributos"],
        [
            ["ROL", "id_rol, nombre_rol, descripcion"],
            ["USUARIO", "id_usuario, id_rol, nombres, apellidos, correo, estado"],
            ["CLIENTE", "id_cliente, agrupador, nit_oracle, nombre_cliente, tipo_cliente, ciudad, direccion, ejecutivo_cuenta, fecha_reforma, cliente_reforma, estado"],
            ["CENTRO", "id_centro, id_cliente, codigo_centro, nombre_centro"],
            ["PRODUCTO", "id_producto, codigo_producto, nombre_producto, tipo_producto, tipo_cliente, tipo_baremo, factor_volumetrico, moneda"],
            ["PAÍS", "codigo_pais, nombre_pais"],
            ["CÓDIGO_POSTAL", "id_codigo_postal, codigo_pais, codigo_postal, ciudad"],
            ["ZONA_TARIFARIA", "id_zona, codigo_zona, nombre_zona"],
            ["PUNTO_VENTA", "id_punto_venta, codigo_crr, nombre_punto"],
            ["TARIFA", "id_tarifa, id_cliente, codigo_tarifa, tipo_tarifa, naturaleza, estado"],
            ["VIGENCIA", "id_vigencia, id_tarifa, fecha_desde, fecha_hasta, estado"],
            ["BAREMO", "id_baremo, id_vigencia, id_producto, numero_baremo, tipo_baremo, valor_fijo, valor_minimo"],
            ["DETALLE_BAREMO", "id_detalle, id_baremo, hasta_kg, importe, sobrepeso, cop_unidad, fraccion, porcentaje"],
            ["RUTA", "id_ruta, id_vigencia, id_producto, id_baremo, pais_origen, id_cp_origen, pais_destino, id_cp_destino, conversion_vol, moneda, llave_porte"],
            ["SOLICITUD", "id_solicitud, id_cliente, id_usuario_registro, tipo_solicitud, canal_recepcion, fecha_solicitud, estado, observaciones"],
            ["ARCHIVO_INSUMO", "id_archivo, id_solicitud, nombre_archivo, tipo_insumo, ruta_almacenamiento, fecha_carga, hash_integridad"],
            ["FICHERO_CSV", "id_fichero, id_solicitud, tipo_fichero, nombre_fichero, separador, fecha_generacion, estado_validacion, ruta_archivo"],
            ["REGLA_VALIDACIÓN", "id_regla, tipo_fichero, nombre_campo, tipo_dato, longitud, obligatorio, expresion_regla, mensaje_error"],
            ["RESULTADO_VALIDACIÓN", "id_resultado, id_fichero, id_regla, fila_afectada, resultado, detalle"],
            ["CARGUE", "id_cargue, id_fichero, id_usuario_carga, id_usuario_aprueba, fecha_cargue, medio_cargue, resultado, log_sistema, registro_sox"],
            ["DESCUENTO_TARIFA", "id_descuento, id_cliente, id_centro, id_producto, id_punto_venta, id_zona, concepto_facturable, desde_kg, hasta_kg, descuento, fecha_desde, fecha_hasta, fecha_baja"],
            ["MÍNIMA_DESPACHO", "id_minima, id_cliente, id_centro, id_producto, rango_kg, minimo, baremo, fecha_desde, fecha_hasta, fecha_baja"],
            ["CARGO_MANEJO", "id_cargo, id_cliente, id_centro, id_producto, tasa_manejo, minimo, fecha_desde, fecha_hasta, fecha_baja"],
        ],
    )
    note(doc, "Los tamaños de código (agrupador 8, centro 2, producto 4, país 3, postal 6) siguen los lineamientos del sistema destino.")

    # ---------- 2 ----------
    h1(doc, "2. Determine las llaves primarias y foráneas")
    body(
        doc,
        "La llave primaria (PK) identifica de forma única cada ocurrencia. La llave foránea (FK) materializa la relación 1:N hacia la entidad padre. Las llaves únicas de negocio (UK) reproducen códigos que el sistema destino ya exige como identificadores (agrupador, código de producto, CRR).",
    )
    caption(doc, "Tabla", 3, "Llaves primarias y foráneas")
    add_table(
        doc,
        ["Entidad", "Llave primaria (PK)", "Llaves foráneas (FK)"],
        [
            ["ROL", "id_rol", "—"],
            ["USUARIO", "id_usuario", "id_rol → ROL"],
            ["CLIENTE", "id_cliente", "—"],
            ["CENTRO", "id_centro", "id_cliente → CLIENTE"],
            ["PRODUCTO", "id_producto", "—"],
            ["PAÍS", "codigo_pais", "—"],
            ["CÓDIGO_POSTAL", "id_codigo_postal", "codigo_pais → PAÍS"],
            ["ZONA_TARIFARIA", "id_zona", "—"],
            ["PUNTO_VENTA", "id_punto_venta", "—"],
            ["TARIFA", "id_tarifa", "id_cliente → CLIENTE (nulo en tarifa general B2C)"],
            ["VIGENCIA", "id_vigencia", "id_tarifa → TARIFA"],
            ["BAREMO", "id_baremo", "id_vigencia → VIGENCIA; id_producto → PRODUCTO"],
            ["DETALLE_BAREMO", "id_detalle", "id_baremo → BAREMO"],
            ["RUTA", "id_ruta", "id_vigencia → VIGENCIA; id_producto → PRODUCTO; id_baremo → BAREMO; pais_origen → PAÍS; pais_destino → PAÍS; id_cp_origen → CÓDIGO_POSTAL; id_cp_destino → CÓDIGO_POSTAL"],
            ["SOLICITUD", "id_solicitud", "id_cliente → CLIENTE; id_usuario_registro → USUARIO"],
            ["ARCHIVO_INSUMO", "id_archivo", "id_solicitud → SOLICITUD"],
            ["FICHERO_CSV", "id_fichero", "id_solicitud → SOLICITUD"],
            ["REGLA_VALIDACIÓN", "id_regla", "—"],
            ["RESULTADO_VALIDACIÓN", "id_resultado", "id_fichero → FICHERO_CSV; id_regla → REGLA_VALIDACIÓN"],
            ["CARGUE", "id_cargue", "id_fichero → FICHERO_CSV; id_usuario_carga → USUARIO; id_usuario_aprueba → USUARIO"],
            ["DESCUENTO_TARIFA", "id_descuento", "id_cliente → CLIENTE; id_centro → CENTRO; id_producto → PRODUCTO; id_punto_venta → PUNTO_VENTA; id_zona → ZONA_TARIFARIA"],
            ["MÍNIMA_DESPACHO", "id_minima", "id_cliente → CLIENTE; id_centro → CENTRO; id_producto → PRODUCTO"],
            ["CARGO_MANEJO", "id_cargo", "id_cliente → CLIENTE; id_centro → CENTRO; id_producto → PRODUCTO"],
        ],
    )
    note(doc, "UK de negocio: CLIENTE.agrupador; PRODUCTO.codigo_producto; CÓDIGO_POSTAL.codigo_postal; PUNTO_VENTA.codigo_crr; ZONA_TARIFARIA.codigo_zona.")

    # ---------- 3 ----------
    h1(doc, "3. Elabore el diagrama entidad-relación (DER)")
    body(
        doc,
        "El DER se elaboró en notación de Chen: rectángulos para entidades, rombos para relaciones y cardinalidad 1:N sobre las líneas. El eje de negocio es CLIENTE → TARIFA → VIGENCIA → (RUTA, BAREMO). El eje de automatización es SOLICITUD → ARCHIVO_INSUMO → FICHERO_CSV → CARGUE.",
    )
    body(
        doc,
        "El archivo editable para Draw.io / diagrams.net se entrega junto con este documento: docs/diagramas/DER_parametrizacion_tarifaria.drawio.",
        first=True,
    )
    p = doc.add_paragraph()
    pf(p, align="center", first=False)
    p.add_run().add_picture(str(FIG_CHEN), width=Inches(6.5))
    caption(
        doc,
        "Figura",
        1,
        "Diagrama entidad-relación (DER) del sistema de automatización tarifaria, notación de Chen. Archivo editable: DER_parametrizacion_tarifaria.drawio.",
    )

    # ---------- 4 ----------
    h1(doc, "4. Construya el modelo relacional (MR)")
    body(
        doc,
        "El modelo relacional traduce el DER a relaciones (tablas). La PK se subraya en el esquema; las FK se marcan en cursiva. Cada FK referencia la PK de la tabla padre y materializa una relación 1:N.",
    )
    body(
        doc,
        "El archivo editable del MER / modelo relacional (tablas con PK y FK) es docs/diagramas/MER_modelo_relacional.drawio.",
    )

    caption(doc, "Tabla", 4, "Esquema del modelo relacional")
    add_table(
        doc,
        ["Relación (tabla)", "Esquema (PK subrayada de forma nominal; FK indicada)"],
        [
            ["ROL", "ROL (id_rol, nombre_rol, descripcion)"],
            ["USUARIO", "USUARIO (id_usuario, id_rol, nombres, apellidos, correo, estado)"],
            ["CLIENTE", "CLIENTE (id_cliente, agrupador, nit_oracle, nombre_cliente, tipo_cliente, ciudad, direccion, ejecutivo_cuenta, fecha_reforma, cliente_reforma, estado)"],
            ["CENTRO", "CENTRO (id_centro, id_cliente, codigo_centro, nombre_centro)"],
            ["PRODUCTO", "PRODUCTO (id_producto, codigo_producto, nombre_producto, tipo_producto, tipo_cliente, tipo_baremo, factor_volumetrico, moneda)"],
            ["PAÍS", "PAÍS (codigo_pais, nombre_pais)"],
            ["CÓDIGO_POSTAL", "CÓDIGO_POSTAL (id_codigo_postal, codigo_pais, codigo_postal, ciudad)"],
            ["ZONA_TARIFARIA", "ZONA_TARIFARIA (id_zona, codigo_zona, nombre_zona)"],
            ["PUNTO_VENTA", "PUNTO_VENTA (id_punto_venta, codigo_crr, nombre_punto)"],
            ["TARIFA", "TARIFA (id_tarifa, id_cliente, codigo_tarifa, tipo_tarifa, naturaleza, estado)"],
            ["VIGENCIA", "VIGENCIA (id_vigencia, id_tarifa, fecha_desde, fecha_hasta, estado)"],
            ["BAREMO", "BAREMO (id_baremo, id_vigencia, id_producto, numero_baremo, tipo_baremo, valor_fijo, valor_minimo)"],
            ["DETALLE_BAREMO", "DETALLE_BAREMO (id_detalle, id_baremo, hasta_kg, importe, sobrepeso, cop_unidad, fraccion, porcentaje)"],
            ["RUTA", "RUTA (id_ruta, id_vigencia, id_producto, id_baremo, pais_origen, id_cp_origen, pais_destino, id_cp_destino, conversion_vol, moneda, llave_porte)"],
            ["SOLICITUD", "SOLICITUD (id_solicitud, id_cliente, id_usuario_registro, tipo_solicitud, canal_recepcion, fecha_solicitud, estado, observaciones)"],
            ["ARCHIVO_INSUMO", "ARCHIVO_INSUMO (id_archivo, id_solicitud, nombre_archivo, tipo_insumo, ruta_almacenamiento, fecha_carga, hash_integridad)"],
            ["FICHERO_CSV", "FICHERO_CSV (id_fichero, id_solicitud, tipo_fichero, nombre_fichero, separador, fecha_generacion, estado_validacion, ruta_archivo)"],
            ["REGLA_VALIDACIÓN", "REGLA_VALIDACIÓN (id_regla, tipo_fichero, nombre_campo, tipo_dato, longitud, obligatorio, expresion_regla, mensaje_error)"],
            ["RESULTADO_VALIDACIÓN", "RESULTADO_VALIDACIÓN (id_resultado, id_fichero, id_regla, fila_afectada, resultado, detalle)"],
            ["CARGUE", "CARGUE (id_cargue, id_fichero, id_usuario_carga, id_usuario_aprueba, fecha_cargue, medio_cargue, resultado, log_sistema, registro_sox)"],
            ["DESCUENTO_TARIFA", "DESCUENTO_TARIFA (id_descuento, id_cliente, id_centro, id_producto, id_punto_venta, id_zona, concepto_facturable, desde_kg, hasta_kg, descuento, fecha_desde, fecha_hasta, fecha_baja)"],
            ["MÍNIMA_DESPACHO", "MÍNIMA_DESPACHO (id_minima, id_cliente, id_centro, id_producto, rango_kg, minimo, baremo, fecha_desde, fecha_hasta, fecha_baja)"],
            ["CARGO_MANEJO", "CARGO_MANEJO (id_cargo, id_cliente, id_centro, id_producto, tasa_manejo, minimo, fecha_desde, fecha_hasta, fecha_baja)"],
        ],
    )
    note(doc, "El primer atributo de cada esquema es la PK. Los atributos cuyo nombre empieza por id_ (distintos de la PK) o pais_/codigo_pais son FK, salvo id_zona, id_punto_venta, id_producto e id_cliente cuando actúan como PK de su propia tabla.")

    p = doc.add_paragraph()
    pf(p, align="center", first=False)
    p.add_run().add_picture(str(FIG_CROW), width=Inches(6.5))
    caption(
        doc,
        "Figura",
        2,
        "Modelo relacional (MR) en notación Crow’s Foot, con PK y FK. Archivo editable: MER_modelo_relacional.drawio.",
    )

    h2(doc, "4.1 Integridad referencial")
    body(doc, "1. Unicidad de ruta: no se repite la combinación vigencia + producto + origen + destino.")
    body(doc, "2. Dependencia ruta-baremo: el cargue de RUTAS exige el fichero hermano de BAREMOS, y a la inversa.")
    body(doc, "3. Vigencia: si el producto ya existe en la vigencia, se crea una vigencia nueva; no se borra histórico.")
    body(doc, "4. Fechas de reforma: fecha_hasta ≥ fecha_desde; fecha_baja inactiva y conserva el histórico.")
    body(doc, "5. Separación de funciones: id_usuario_carga e id_usuario_aprueba no deben coincidir en el mismo CARGUE.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    build()
