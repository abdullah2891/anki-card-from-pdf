from typing import Generator
import argparse
import multiprocessing
from utils import parse_answer_question, generate_prompt, parse_pdf, parse_page_range
from llm_helper import run_llm_model


def main():
    parser = argparse.ArgumentParser(description="Process a PDF file input.")
    parser.add_argument(
        "file", type=argparse.FileType("rb"), help="Path to the input PDF file"
    )
    parser.add_argument(
        "--range",
        type=str,
        help="Range of pages to process (e.g., '1-3,5,7-9')",
        default=None,
    )

    args = parser.parse_args()

    file_handler = args.file

    pdf_pages = parse_pdf(file_handler)

    if args.range:
        selected_pages = parse_page_range(args.range)
        partial_list_pdf_pages = []

        for range in selected_pages:
            start = range["start"]
            end = range["end"]
            partial_list_pdf_pages += pdf_pages[start:end]

        pdf_pages = partial_list_pdf_pages

    else:
        print("Processing entire PDF.")

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.imap(run_llm_model, pdf_pages)

        for r in results:
            parsed = parse_answer_question(r)
            print(parsed)


if __name__ == "__main__":
    main()
