from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.enums import *
from reportlab.platypus import *
from deep_translator import GoogleTranslator
import Config as ConfigData
import os

output_path = "./CV_Generados"
os.makedirs(output_path, exist_ok=True)


def generate_CV_PDF(index):

    # ------------------ LOAD INFO DATA -------------------------------- #
    full_Name = "David Steven Diaz Perez"
    address = "Cra 8H #173-84, Bogotá, Colombia"
    phone = "+57 310 270 5787"
    email = "daivvdiz@gmail.com"

    # ------------------ LOAD EDUCATION DATA -------------------------------- #
    education_selected = ConfigData.education_data

    # ------------------ LOAD EXPERIENCE DATA -------------------------------- #
    experience_selected = ConfigData.experience_data

    # ------------------ LOAD PERSONAL INFO DATA -------------------------------- #
    personal_selected = ConfigData.personal_data

    # ------------------ LOAD LANGUAJES DATA -------------------------------- #
    languajes_selected = ConfigData.languajes_data

    # Crear documento PDF
    file_ID = "EN" if index else "ES"
    filename = os.path.join(
        output_path, f"CV_{str.upper(full_Name).replace(' ', '_')}_{file_ID}.pdf"
    )

    if os.path.exists(filename):
        os.remove(filename)

    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    default_style = ParagraphStyle(
        name="Default",
        fontName="Times-Roman",
        fontSize=10,
    )

    story = []

    def translate_Text(text, to="en"):
        translate = GoogleTranslator(source="auto", target=to).translate(text)
        translate = translate.replace("Aunt Portal", "TIA Portal")
        return translate

    def add_Title(title_name):
        style = ParagraphStyle(
            name="CustomTitle",
            fontName="Times-Bold",
            fontSize=12,
            alignment=TA_CENTER,
        )
        title_name = str.upper(title_name)
        story.append(Paragraph(title_name, style))
        story.append(Spacer(1, 12))

    def add_Info(address, phone, email):

        style = ParagraphStyle(
            name="CustomTitle",
            fontName="Times-Roman",
            fontSize=10,
            alignment=TA_CENTER,
        )

        info = address + " - " + phone + " - " + email

        story.append(Paragraph(info, style))
        story.append(Spacer(2, 12))

    def add_Section(section_name):
        section_name = translate_Text(section_name) if index else section_name

        style = ParagraphStyle(
            name=section_name,
            fontName="Times-Bold",
            fontSize=10,
            alignment=TA_LEFT,
        )
        story.append(Paragraph(str.upper(section_name), style))
        add_Separator()

    def add_Separator():
        story.append(HRFlowable(width="100%", thickness=1, color="black"))
        story.append(Spacer(1, 12))

    def add_Two_Columns(left_text, right_text, left_style=None, right_style=None):

        default_left_style = ParagraphStyle(
            name="Default",
            fontName="Times-Roman",
            fontSize=10,
            alignment=TA_LEFT,
        )
        default_right_style = ParagraphStyle(
            name="Default", fontName="Times-Roman", fontSize=10, alignment=TA_RIGHT
        )

        left_paragraph = Paragraph(left_text, left_style or default_left_style)
        right_paragraph = Paragraph(right_text, right_style or default_right_style)

        table = Table([[left_paragraph, right_paragraph]], colWidths=["*", "*"])
        table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (0, 0), "LEFT"),
                    ("VALIGN", (1, 0), (1, 0), "CENTER"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        story.append(table)

    def add_List(items):
        for item in items:
            item = translate_Text(item) if index else item
            story.append(Paragraph(f"• {item}", default_style))

    # Personal Info
    add_Title(full_Name)
    add_Info(address, phone, email)

    # Education Info
    add_Section("Educación")

    for r in education_selected:
        institute, location, program, dates, knowledge = r

        institute = translate_Text(institute) if index else institute
        location = translate_Text(location) if index else location
        program = translate_Text(program) if index else program

        institute = str.upper(institute)

        add_Two_Columns(
            institute, location, ParagraphStyle(name="Left", fontName="Times-Bold")
        )
        add_Two_Columns(
            program, dates, ParagraphStyle(name="Left", fontName="Times-Italic")
        )
        add_List(knowledge)

        story.append(Spacer(1, 12))

    # Experience Info
    add_Section("Experiencia")

    for r in experience_selected:
        company, location, industry, role, dates, tasks = r

        location = translate_Text(location) if index else location
        industry = translate_Text(industry) if index else industry
        role = translate_Text(role) if index else role

        company = str.upper(company)
        add_Two_Columns(
            company, location, ParagraphStyle(name="Left", fontName="Times-Bold")
        )
        add_Two_Columns(industry, " ")
        add_Two_Columns(
            role, dates, ParagraphStyle(name="Left", fontName="Times-BoldItalic")
        )
        add_List(tasks)
        story.append(Spacer(1, 12))

    # Personal Info
    add_Section("Información Personal")
    add_List(personal_selected)

    # Languajes Info
    story.append(PageBreak())
    add_Section("Idiomas")
    add_List(languajes_selected)

    # Generar PDF
    doc.build(story)
    print(f"✅ ¡CV generado con éxito en el archivo: {filename}!")


if __name__ == "__main__":
    generate_CV_PDF(False)
    generate_CV_PDF(True)
