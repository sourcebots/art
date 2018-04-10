from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import SvgRenderer

p = canvas.Canvas("file.pdf")
p.setPageSize((297, 210))
p.drawString(0, 0, "Yes")
p.showPage()
p.drawString(0, 0, "Yes")
p.save()
