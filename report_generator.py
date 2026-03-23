from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_report(role, score, matching, missing, roadmap):

    filename = "career_report.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "CareerRAG Pro Report")

    y -= 40
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Target Role: {role}")
    y -= 20

    c.drawString(50, y, f"Career Readiness Score: {score}%")

    y -= 40
    c.drawString(50, y, "Matching Skills")

    y -= 20
    for skill in matching:
        c.drawString(70, y, f"- {skill}")
        y -= 15

    y -= 20
    c.drawString(50, y, "Missing Skills")

    y -= 20
    for skill in missing:
        c.drawString(70, y, f"- {skill}")
        y -= 15

    y -= 20
    c.drawString(50, y, "Learning Roadmap")

    y -= 20
    for step in roadmap:
        c.drawString(70, y, f"- {step}")
        y -= 15

    c.save()

    return filename