# python -m pip install -r .\requirements.txt
# python .\annotate.py .\questions .\annotatedPdfs

import io
import PyPDF2
from reportlab.pdfgen import canvas
import sys
import os

def annotate_pdf(input_path, output_path):
    # Get the filename (without the extension) for the annotation
    filename = os.path.basename(input_path).replace(".pdf", "")

    # Read the input PDF
    with open(input_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            packet = io.BytesIO()

            # Determine page dimensions and create a new PDF with reportlab
            page_width = page["/MediaBox"][2]
            page_height = page["/MediaBox"][3]

            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            can.drawString(page_width - 60, 20, filename)  # You may need to adjust positioning here
            can.save()

            # Move buffer position to the beginning
            packet.seek(0)
            new_pdf = PyPDF2.PdfReader(packet)
            page.merge_page(new_pdf.pages[0])
            writer.add_page(page)

        # Save the annotated PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

if __name__ == "__main__":
    # Command-line arguments
    source_folder = sys.argv[1]
    dest_folder = sys.argv[2]

    # Ensure the destination folder exists
    os.makedirs(dest_folder, exist_ok=True)

    # Iterate over each PDF in the source folder
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".pdf"):
            input_path = os.path.join(source_folder, file_name)
            output_path = os.path.join(dest_folder, file_name)
            annotate_pdf(input_path, output_path)
