# PDF Comparison & Document Analysis Tool

A Python command-line tool that compares two PDF files and determines whether they are identical at the file level.

## Milestone 1 — File Comparison

The first milestone focuses on comparing two PDF files using **SHA-1 hashing**.

The program:

* Accepts two PDF files
* Displays their filenames
* Reads both files in binary mode
* Generates a SHA-1 hash for each file
* Compares the hashes
* Determines whether the files are exactly identical

## Technologies Used

* Python
* `pypdf`
* `hashlib`
* `os`

## How It Works

Each PDF file is read in binary chunks and passed through Python's `hashlib.sha1()` hashing algorithm.

The generated hashes act as digital fingerprints for the files.

If both hashes are equal, the PDF files contain exactly the same binary data.

If the hashes are different, the files are not identical.

## Usage

Set the paths of the two PDF files inside the program:

```python
PDF1_PATH = "pdf1.pdf"
PDF2_PATH = "pdf2.pdf"
```

Run the program:

```bash
python main.py
```

The comparison result will be displayed in the terminal.

## Example Output

```text
PDF Comparison Report
=====================

File A: pdf1.pdf
File B: pdf2.pdf

Files are identical: False
```

## What I Learned

During this milestone, I practiced:

* Reading files in binary mode
* Processing files in chunks
* Working with SHA-1 hashes
* Comparing file fingerprints
* Using Python classes and methods
* Working with file paths and filenames
* Breaking a larger project into smaller implementation milestones

## Project Status

**Milestone 1 completed:** exact PDF file comparison using hashing.

Further document analysis functionality will be added in future milestones.
