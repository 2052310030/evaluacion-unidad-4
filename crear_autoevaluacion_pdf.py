from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def crear_pdf():
    documento = SimpleDocTemplate(
        "Autoevaluacion_Evaluacion_U4.pdf",
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle(
        "TituloPersonalizado", parent=estilos["Title"], alignment=TA_CENTER,
        textColor=colors.HexColor("#17324d"), fontSize=18, spaceAfter=16
    )
    normal = ParagraphStyle("Celda", parent=estilos["BodyText"], fontSize=9, leading=12)
    encabezado = ParagraphStyle(
        "Encabezado", parent=normal, alignment=TA_CENTER,
        textColor=colors.white, fontName="Helvetica-Bold"
    )

    contenido = [
        Paragraph("Autoevaluación - Evaluación Unidad 4", titulo),
        Paragraph("<b>Matrícula:</b> ____________________", estilos["BodyText"]),
        Paragraph("<b>Nombre:</b> Ximena Herrera Olvera", estilos["BodyText"]),
        Spacer(1, 14),
    ]
    filas = [
        [Paragraph("Criterio", encabezado), Paragraph("Autoevaluación", encabezado), Paragraph("Motivos", encabezado)],
        [Paragraph("Entrega en tiempo y forma (Git)", normal), "10", Paragraph("El repositorio se entregó organizado, con archivos separados, commits claros y documentación por apartado.", normal)],
        [Paragraph("Pruebas unitarias (pytest)", normal), "10", Paragraph("Se probaron registro, actualización, eliminación, costos inválidos, campos vacíos y servicios duplicados mediante AAA y F.I.R.S.T.", normal)],
        [Paragraph("Manejo de excepciones", normal), "10", Paragraph("Se utilizaron excepciones personalizadas y bloques try/except/else/finally con mensajes claros.", normal)],
        [Paragraph("Debugging con pdb", normal), "10", Paragraph("Se agregaron breakpoints, se inspeccionaron variables y se documentaron los comandos utilizados.", normal)],
        [Paragraph("Proyecto CRUD (Tkinter + MySQL + SOLID)", normal), "10", Paragraph("El CRUD permite registrar, consultar, actualizar y eliminar; usa una GUI funcional, MySQL y clases con responsabilidades separadas.", normal)],
    ]
    tabla = Table(filas, colWidths=[4.4 * cm, 2.7 * cm, 10.4 * cm], repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324d")),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#8a99a8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f7")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    contenido.append(tabla)
    contenido.append(Spacer(1, 12))
    contenido.append(Paragraph(
        "Nota: revisa las calificaciones y motivos antes de entregar; deben coincidir con las evidencias realizadas.",
        estilos["Italic"],
    ))
    documento.build(contenido)


if __name__ == "__main__":
    crear_pdf()
