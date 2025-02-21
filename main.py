from typing import Generator
import argparse
import PyPDF2


def parse_pdf(fh) -> Generator:
    with fh as f:
        reader = PyPDF2.PdfReader(f)
        return [page for page in reader.pages if page.extract_text()]


def main():
    parser = argparse.ArgumentParser(description="Process a PDF file input.")
    parser.add_argument("file", type=argparse.FileType('rb'), help="Path to the input PDF file")
    args = parser.parse_args()
    file_handler = args.file

    pdf_file_generator = parse_pdf(file_handler)

    for page in pdf_file_generator:
        print(page.extract_text())
    
if __name__ == "__main__":
    main()

