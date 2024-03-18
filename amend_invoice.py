import io
from tkinter import filedialog, Tk
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def add_text_to_pdf(text_block1, text_block2, input_pdf_path, x1, y1, y2):
    existing_pdf = PdfReader(open(input_pdf_path, 'rb'))
    total_pages = len(existing_pdf.pages)
    try:
        output_pdf_path = '_' + input_pdf_path[-46:]
    except:
        output_pdf_path = '_Sales Invoice.pdf'
    output = PdfWriter()
    packet = io.BytesIO()
    for page_num in range(total_pages):
        can = canvas.Canvas(packet, pagesize=A4)
        if page_num == 0:
            can.setFont('Helvetica-Bold', 8)
            for i, line in enumerate(text_block1):
                if i == 0:
                    can.drawString(x1, y1 - i * 12, line)
                else:
                    can.setFont("Helvetica", 8)
                    can.drawString(x1, y1 - i * 12, line)
        if page_num == total_pages - 1:
            can.setFont('Helvetica-Bold', 12)
            center_x = A4[0] / 2
            for i, line in enumerate(text_block2):
                text_block2_width = can.stringWidth(line, 'Helvetica-Bold', 12)
                start_x = center_x - (text_block2_width / 2)
                can.drawString(start_x, y2 - i * 14, line)
        can.save()
        packet.seek(0)
        new_pdf = PdfReader(packet)
        if new_pdf.pages:
            page = existing_pdf.pages[page_num]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)
        else:
            output.add_page(existing_pdf.pages[page_num])
    with open(output_pdf_path, 'wb') as outfile:
        output.write(outfile)


text_block2 = [
    "I certify that all chemical substances in this shipment comply with all applicable rules or orders ",
    "under TSCA and that I am not offering a chemical substance for entry in violation of TSCA or any ",
    "applicable rule or order under TSCA",
]

text_block1 = ["Manufacturer's Name & Address"]

print()
importer = int(input('1. Ningbo 2. YanTian : '))

if importer == 1:
    text_block1.extend([
        "Factory 1 CO LTD",
        "XXXXXXXXXX, XINCANG TOWN",
        "XXXXXXXXXX, 314299 ZHEJIANG CN"]
    )
elif importer == 2:
    text_block1.extend([
        "Factory 2 Industry inc",
        "XXXXXXXXX Road",
        "XXXXXXXXX Zhongshan",
        "Guangdong, China"
    ])
else:
    print('incorrect port')
    exit()

x1 = 180
y1 = 680
y2 = 100
coordinates = input('enter X1<180>,Y1<680>; Y2<100> or press <enter> to skip ')
if coordinates:
    x1, y1, y2 = map(int, coordinates.split(','))

# root = Tk()
# root.withdraw()
# input_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
input_pdf_path = 'sales_invoice.pdf'
if not input_pdf_path:
    print("No file selected. Exiting.")
    exit()

add_text_to_pdf(text_block1, text_block2, input_pdf_path, x1, y1, y2)
