import pymupdf
import pypdf
import hashlib
from difflib import SequenceMatcher
import os

PDF1_PATH = '/Users/paunbogdan/PycharmProjects/Projects/Portofolio/PDF Comparison & Document Analysis Tool/pdf1.pdf'
PDF2_PATH = '/Users/paunbogdan/PycharmProjects/Projects/Portofolio/PDF Comparison & Document Analysis Tool/pdf2.pdf'

class PDFComparisonTool:

    def __init__(self, pdf1, pdf2):
        self.pdf1 = pdf1
        self.pdf2 = pdf2
        print("""\nPDF Comparison Report
=====================
        """)

    def file_match(self):
        pdf1 = pypdf.PdfReader(self.pdf1)
        pdf2 = pypdf.PdfReader(self.pdf2)

        # We get the file name with the os module
        pdf1_name = os.path.basename(PDF1_PATH)
        pdf2_name = os.path.basename(PDF2_PATH)

        print(f"File A: {pdf1_name}\nFile B: {pdf2_name}\n")

        hash_pdf1, hash_pdf2 = self.get_hash_file()


        matching_message = "Exact file match: "
        if hash_pdf1 != hash_pdf2:
            matching_message += "No"
        else:
            matching_message += "Yes"

        print(matching_message)


    # This function here calculates the hash of the PDF files so we can compare them later on
    def get_hash_file(self):
        hash1 = hashlib.sha1()
        hash2 = hashlib.sha1()

        with open(self.pdf1, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                hash1.update(chunk)

        with open(self.pdf2, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                hash2.update(chunk)

        msg1, msg2 = hash1.hexdigest(), hash2.hexdigest()
        return msg1, msg2


pdf_comparison_tool = PDFComparisonTool(PDF1_PATH, PDF2_PATH)

pdf_comparison_tool.file_match()