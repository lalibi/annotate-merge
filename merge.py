# python -m pip install -r .\requirements.txt
# python .\merge.py .\annotatedPdfs\ final.pdf

import PyPDF2
import os
import sys

def merge_pdfs(pdf_dir, output_filename):
    pdf_writer = PyPDF2.PdfWriter()

    # Get all PDF files in the given directory
    files = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]

    for file in files:
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])

    with open(output_filename, 'wb') as merged_pdf:
        pdf_writer.write(merged_pdf)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge.py <PDF_DIRECTORY> <OUTPUT_FILENAME>")
        sys.exit(1)

    pdf_dir = sys.argv[1]
    output_filename = sys.argv[2]

    # Merge the PDFs into a single file
    merge_pdfs(pdf_dir, output_filename)
