# PDF Comparison & Document Analysis Tool

A Python command-line tool for comparing two PDF files and analyzing how similar they are.

The current version performs both an exact file comparison and an overall text similarity comparison.

## Features

- Compare two PDF files
- Display both filenames
- Generate SHA-1 hashes for each file
- Detect whether the files are exactly identical
- Count the number of pages in each PDF
- Extract text from all pages
- Calculate overall text similarity using `SequenceMatcher`
- Display a simple comparison report in the terminal

## Technologies Used

- Python
- `pypdf`
- `hashlib`
- `difflib.SequenceMatcher`
- `os`

## How It Works

### Exact File Comparison

Each PDF file is read in binary mode and processed using SHA-1 hashing.

The generated hashes act as digital fingerprints for the files.

If both hashes are equal, the files are exactly identical.

If the hashes are different, the files are not exact copies.

### Document Summary

The program reads both PDF files using `PdfReader` and determines the number of pages in each document, while also returning the overall text similarity between the extracted text of both PDF files.

Example:

```text
Pages in File A: 5
Pages in File B: 6
Overall text similarity: 89.37%
