import pymupdf
from pypdf import PdfReader
import hashlib
from difflib import SequenceMatcher
import os

PDF1_PATH = '/Users/paunbogdan/PycharmProjects/Projects/Portofolio/PDF Comparison & Document Analysis Tool/pdf1.pdf'
PDF2_PATH = '/Users/paunbogdan/PycharmProjects/Projects/Portofolio/PDF Comparison & Document Analysis Tool/pdf2.pdf'

class PDFComparisonTool:

    def __init__(self, pdf1, pdf2):
        self.pages_pdf2 = None
        self.pages_pdf1 = None
        self.pdf1 = pdf1
        self.pdf2 = pdf2
        print("""\nPDF Comparison Report
=====================
        """)

    def file_match(self):

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

    def document_summary(self):
        print("""\nDocument Summary
----------------""")

        # Reading both pdf files
        reader1 = PdfReader(self.pdf1)
        reader2 = PdfReader(self.pdf2)

        # Getting the number of pages in each pdf file
        pages_pdf1 = len(reader1.pages)
        self.pages_pdf1 = pages_pdf1

        pages_pdf2 = len(reader2.pages)
        self.pages_pdf2 = pages_pdf2

        print(f"Pages in file A: {pages_pdf1}")
        print(f"Pages in file B: {pages_pdf2}")

        # Get the similarity of the two PDF's

        pdf1_text = self.extract_all_text_from_pdf(reader1)
        pdf2_text = self.extract_all_text_from_pdf(reader2)

        overall_similarity = SequenceMatcher(None, pdf1_text, pdf2_text)
        print(f"Overall text similarity: {overall_similarity.ratio() * 100:.2f}%")

    @staticmethod
    def extract_all_text_from_pdf(pdf):
        text = ""
        for page in range(len(pdf.pages)):
            text += pdf.pages[page].extract_text()

        return text


pdf_comparison_tool = PDFComparisonTool(PDF1_PATH, PDF2_PATH)

pdf_comparison_tool.file_match()
pdf_comparison_tool.document_summary()