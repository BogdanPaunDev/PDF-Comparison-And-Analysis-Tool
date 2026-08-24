from enum import nonmember

from pypdf import PdfReader
import hashlib
from difflib import SequenceMatcher
import os
import argparse

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


class PDFComparisonTool:

    def __init__(self, pdf1, pdf2):
        self.reader1 = PdfReader(pdf1)
        self.reader2 = PdfReader(pdf2)
        self.pdf1 = pdf1
        self.pdf2 = pdf2
        self.pages_changed = 0
        self.count_additional_pages = 0
        print("""\nPDF Comparison Report
=====================
        """)

    def file_match(self):

        # We get the file name with the os module
        pdf1_name = os.path.basename(self.pdf1)
        pdf2_name = os.path.basename(self.pdf2)

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

        pages_pdf1 = len(self.reader1.pages)

        pages_pdf2 = len(self.reader2.pages)

        print(f"Pages in file A: {pages_pdf1}")
        print(f"Pages in file B: {pages_pdf2}")

        # Get the similarity of the two PDF's

        pdf1_text = self.extract_all_text_from_pdf(self.reader1)
        pdf2_text = self.extract_all_text_from_pdf(self.reader2)

        overall_similarity = SequenceMatcher(None, pdf1_text, pdf2_text)
        print(f"Overall text similarity: {overall_similarity.ratio() * 100:.2f}%")

    @staticmethod
    def extract_all_text_from_pdf(pdf):
        text = ""
        for page in range(len(pdf.pages)):
            text += pdf.pages[page].extract_text()

        return text

    def page_comparison(self):
        print("""
Page Comparison
---------------""")

        min_length = min(len(self.reader1.pages), len(self.reader2.pages))

        pages_modified = []
        for page in range(min_length):
            a = self.reader1.pages[page].extract_text()
            b = self.reader2.pages[page].extract_text()

            ratio = SequenceMatcher(None, a, b).ratio()

            status = self.switch(ratio)
            print(f"Page {page + 1}: {ratio * 100:.2f}% overall similarity. Status: {status}")
            if status == "Changed" or status == "Minor Changes":
                pages_modified.append(str(page + 1))

        self.pages_changed = len(pages_modified)
        self.pages_modified(pages_modified)

    @staticmethod
    def switch(percentage):
        if 0.94 <= percentage < 0.99:
            return "Minor Changes"
        elif percentage < 0.94:
            return "Changed"
        else:
            return "Identical"

    @staticmethod
    def pages_modified(pages_changed):
        print("Changed pages: ", end="")
        print(", ".join(pages_changed))

    def page_difference(self):
        print("""Page Count Difference
---------------------""")
        pages_file_a = len(self.reader1.pages)
        pages_file_b = len(self.reader2.pages)

        page_difference = 0
        min_pages = min(pages_file_a, pages_file_b)

        if pages_file_a > pages_file_b:
            page_difference = pages_file_a - pages_file_b
            print(f"File A contains {page_difference} additional pages/page:")
        elif pages_file_a < pages_file_b:
            page_difference = pages_file_b - pages_file_a
            print(f"File B contains {page_difference} additional pages/page:")
        else:
            print("Both files have the same number of pages.")
            return

        self.count_additional_pages = page_difference

        additional_pages = []

        for page in range(page_difference):
            additional_pages.append(str(min_pages + page + 1))

        print("- Page: " + ", ".join(additional_pages))

    def text_differences(self):
        print("""
Text Differences
----------------\n""")

        for page_number in range(min(len(self.reader1.pages), len(self.reader2.pages))):
            page_text_a = self.reader1.pages[page_number].extract_text().split()
            page_text_b = self.reader2.pages[page_number].extract_text().split()

            pages_differences = SequenceMatcher(None, page_text_a, page_text_b)

            if pages_differences.ratio() < 1:
                print("\nPage " + str(page_number + 1) + ":\n")

            for tag, i1, i2, j1, j2 in pages_differences.get_opcodes():

                if tag == "equal":
                    continue

                elif tag == "delete":
                    print(RED + "Removed: " + " ".join(page_text_a[i1:i2]) + RESET)

                elif tag == "insert":
                    print(GREEN + "Added: " + " ".join(page_text_b[j1:j2]) + RESET + "\n")

                elif tag == "replace":
                    print(RED + "Removed: " + " ".join(page_text_a[i1:i2]) + RESET)
                    print(GREEN + "Added: " + " ".join(page_text_b[j1:j2]) + RESET + "\n")

    def final_result(self):

        pdf1_text = self.extract_all_text_from_pdf(self.reader1)
        pdf2_text = self.extract_all_text_from_pdf(self.reader2)

        if pdf1_text == pdf2_text and len(self.reader1.pages) == len(self.reader2.pages):
            print("Exact Match: Yes")
        else:
            print("Exact Match: No")

        print(f"Text Similarity: {round(SequenceMatcher(None, pdf1_text, pdf2_text).ratio() * 100, 2)}%")
        print("Pages Changed: " + str(self.pages_changed))
        print("Additional Pages: " + str(self.count_additional_pages))


def valid_pdf(pdf):
    if not os.path.exists(pdf):
        raise argparse.ArgumentTypeError(f"The {pdf} does not exist. Enter a valid file path.")

    if not os.path.isfile(pdf):
        raise argparse.ArgumentTypeError(f"It seems that the {pdf} is not a file.")

    if not pdf.lower().endswith(".pdf"):
        raise argparse.ArgumentTypeError(f"{pdf} is not a PDF file.")

    return pdf

def main():

    parser = argparse.ArgumentParser(
        description="A PDF comparison tool used to give a complete file match report between the two PDF files provided."
    )

    parser.add_argument('pdf1', type=valid_pdf, help="The path to the first PDF file.")
    parser.add_argument('pdf2', type=valid_pdf, help="The path to the second PDF file.")

    args = parser.parse_args()



    pdf_comparison_tool = PDFComparisonTool(args.pdf1, args.pdf2)

    pdf_comparison_tool.file_match()
    pdf_comparison_tool.document_summary()
    pdf_comparison_tool.page_comparison()
    pdf_comparison_tool.page_difference()
    pdf_comparison_tool.text_differences()
    pdf_comparison_tool.final_result()

if __name__ == "__main__":
    main()



