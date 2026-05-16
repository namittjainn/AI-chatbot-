from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_pdf(filename, title, content):
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, title)

    c.setFont("Helvetica", 11)

    y = 770

    for line in content.split("\n"):
        c.drawString(50, y, line[:100])
        y -= 18

        if y < 50:
            c.showPage()
            y = 800

    c.save()