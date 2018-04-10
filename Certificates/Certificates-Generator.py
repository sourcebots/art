from reportlab.pdfgen import canvas
from svglib.svglib import SvgRenderer

ren = SvgRenderer()
ren.render("Participation.svg")
certificate = ren.finish()

p = canvas.Canvas("file.pdf")
p.setPageSize((297, 210))
p.drawString(0, 0, "Yes")
p.showPage()
p.drawString(0, 0, "Yes")
p.save()
