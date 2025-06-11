from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.enums import *
from reportlab.platypus import *
from deep_translator import GoogleTranslator
import Config as ConfigData
import os

output_path = "C:/Users/David/Downloads/CV_Collection"
os.makedirs(output_path, exist_ok=True)


def generate_CV_PDF(index):

    # ------------------ LOAD INFO DATA -------------------------------- #
    full_Name = "David Steven Diaz Perez"
    info_data = {
        "Email": "daivvdiz@gmail.com",
        "Phone": "+57 310 270 5787",
        "LinkedIn": '<a href="https://www.linkedin.com/in/daivvdiz"><font color="black"><u>LinkedIn</u></font></a>',
        "GitHub": '<a href="https://www.github.com/daivvdiz"><font color="black"><u>GitHub</u></font></a>',
    }

    # ------------------ LOAD PROFESSIONAL PROFILE DATA -------------------------------- #
    profile_data = ConfigData.profile_data

    # ------------------ LOAD EDUCATION DATA -------------------------------- #
    skills_data = ConfigData.skills_data

    # ------------------ LOAD EDUCATION DATA -------------------------------- #
    edducation_data = ConfigData.education_data

    # ------------------ LOAD EXPERIENCE DATA -------------------------------- #
    experience_data = ConfigData.experience_data

    # ------------------ LOAD PERSONAL INFO DATA -------------------------------- #
    personal_data = ConfigData.personal_data

    # ------------------ LOAD PROJECTS DATA -------------------------------- #
    projects_data = ConfigData.projects_data

    # ------------------ LOAD LANGUAJES DATA -------------------------------- #
    languajes_data = ConfigData.languajes_data

    # Crear documento PDF
    file_position = "DATA"
    file_ID = "EN" if index else "ES"
    filename = os.path.join(
        output_path, f"CV_{str.upper(full_Name).replace(' ', '_')}_{file_ID}_{file_position}.pdf"
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
        inputs = ["Aunt Portal", "Pandas", "Matpletlib", "PLCS", "Food Plotlib", "Girub", "Portal Festo", "Tia Portal"]
        outputs = ["TIA Portal", "pandas", "matplotlib", "PLCs", "matplotlib", "GitHub", "Portal, Festo", "TIA Portal"]
        if len(inputs) == len(outputs):
            l = len(inputs)
            if index:
                translate = GoogleTranslator(source="auto", target=to).translate(text)
                for x in range(0, l, 1):
                    translate = translate.replace(inputs[x], outputs[x])
                return translate
            else:
                return text

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

    def add_Info(info_data=None):
        if info_data is None:
            info_data = {}
        if story is None:
            raise ValueError("Debes pasar una lista válida en 'story'.")

        # Estilos
        style = ParagraphStyle(
            name="BasicInfo",
            fontName="Times-Roman",
            fontSize=10,
            alignment=TA_CENTER,
        )

        # Armar línea como "Email: x | LinkedIn: x | GitHub: x"
        items = []
        for key, value in info_data.items():
            items.append(f"{value}")

        info_line = " | ".join(items)

        story.append(Paragraph(info_line, style))
        story.append(Spacer(1, 12))

    def add_Section(section_name):
        section_name = translate_Text(section_name)

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
            name="Default",
            fontName="Times-Roman",
            fontSize=10,
            alignment=TA_RIGHT
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

    def add_List(items, index=None):
        subtitle_style = ParagraphStyle(
            name="Subtitle",
            fontName="Times-Bold",
            fontSize=10,
            alignment=TA_LEFT,
        )

        for n, item in enumerate(items):
            item = translate_Text(item)
            if n == index:
                item = str.upper(item)
                story.append(Paragraph(f"{item}", subtitle_style))
            else:
                story.append(Paragraph(f"• {item}", default_style))

        story.append(Spacer(1, 12))

    # ---------------------------------- BUILD DOCUMENT ----------------------------------- #
    
    # NAME
    add_Title(full_Name)

    # CONTACT INFO
    add_Info(info_data)

    # PROFILE
    add_Section("Perfil Profesional")
    story.append(Paragraph(translate_Text(profile_data), default_style))
    story.append(Spacer(1, 12))

    # SKILLS
    add_Section("Habilidades")
    for r in skills_data:
        add_List(r, 0)

    story.append(PageBreak())

    # EDUCATION
    add_Section("Educación")

    for r in edducation_data:
        institute, location, program, dates, knowledge = r

        institute = translate_Text(institute)
        location = translate_Text(location)
        program = translate_Text(program)

        institute = str.upper(institute)

        add_Two_Columns(
            institute, location, ParagraphStyle(name="Left", fontName="Times-Bold")
        )
        add_Two_Columns(
            program, dates, ParagraphStyle(name="Left", fontName="Times-Italic")
        )
        add_List(knowledge)

    # EXPERIENCE
    add_Section("Experiencia")

    for r in experience_data:
        company, location, industry, role, dates, tasks = r

        location = translate_Text(location)
        industry = translate_Text(industry)
        role = translate_Text(role)

        company = str.upper(company)
        add_Two_Columns(
            company, location, ParagraphStyle(name="Left", fontName="Times-Bold")
        )
        add_Two_Columns(industry, " ")
        add_Two_Columns(
            role, dates, ParagraphStyle(name="Left", fontName="Times-BoldItalic")
        )
        add_List(tasks)

    story.append(PageBreak())

    # PROJECTS
    add_Section("Proyectos personales o académicos")
    for r in projects_data:
        institute, program, name, profile, date, knowledge = r

        institute = translate_Text(institute)
        program = translate_Text(program)
        name = translate_Text(name)
        profile = translate_Text(profile)
        date = translate_Text(date)

        institute = str.upper(institute)

        add_Two_Columns(
            institute, program, ParagraphStyle(name="Left", fontName="Times-Bold")
        )
        add_Two_Columns(
            name, date, ParagraphStyle(name="Left", fontName="Times-Italic")
        )
        add_List(knowledge)

    # LANGUAJES
    add_Section("Idiomas")
    add_List(languajes_data)

    # PERSONAL
    add_Section("Información Personal")
    add_List(personal_data)

    # Generar PDF
    doc.build(story)
    print(f"✅ ¡CV generado con éxito en el archivo: {filename}!")


if __name__ == "__main__":
    generate_CV_PDF(False)
    generate_CV_PDF(True)
