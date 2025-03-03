from typing import Generator
import argparse
import PyPDF2
from data.anki_card_prompt import anki_card_prompt
from data.sample_pdf_page import sample_input_page
import subprocess
import multiprocessing
import re

def parse_answer_question(text):
    faq_list = []
    formatted_output = ""

    if not isinstance(text, str):
        return ""
    
    # Removing separator lines
    text = re.sub(r'\n\+{10,}\n', '\n', text)
    
    # Extracting Q&A pairs
    qa_pairs = re.findall(r'Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|\Z)', text, re.DOTALL)
    for question, answer in qa_pairs:
        faq_list.append({"question": question.strip(), "answer": answer.strip()})
    
    # Extracting bullet point Q&A format
    bullet_qa = re.findall(r'\u2022(.*?)\n(.*?)(?=\n\u2022|\Z)', text, re.DOTALL)
    for question, answer in bullet_qa:
        faq_list.append({"question": question.strip(), "answer": answer.strip()})
    
    # Extracting simple question-answer pairs
    line_qa = re.findall(r'(.*?)\?\s*(.*?)(?=\n[A-Z]|\Z)', text, re.DOTALL)
    for question, answer in line_qa:
        faq_list.append({"question": question.strip() + "?", "answer": answer.strip()})
    
    for pair in faq_list:
        if bool(pair["question"]) and bool(pair["answer"]):
            formatted_output += f"{pair['question']}|{pair['answer']}" + '\n'
    
    return formatted_output



def generate_prompt(prompot_dict,data) -> str:
    '''
    helps to build effective prompt

    '''
    goal = prompot_dict['goal']
    return_format = prompot_dict['return_format']
    warnings = prompot_dict['warnings']


    return f" \n {goal} \n {return_format} \n {warnings} \n {data}" 


def run_llm_model(prompt: str) -> str:
    model = "llama3.2"
    
    # Command to run with shell features (e.g., command substitution)
    command = f'ollama run {model} "{prompt}"'

    # Execute the command, capturing the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check if the command ran successfully
    if result.returncode == 0:
        return result.stdout
    else:
        pass



def parse_pdf(fh) -> Generator:
    with fh as f:
        reader = PyPDF2.PdfReader(f)
        return [generate_prompt(anki_card_prompt, page.extract_text()) for page in reader.pages if page.extract_text()]

def parse_page_range(range_str: str) -> dict:
    '''
        returns list start and end list 
        [
            {
                'start': 20,
                'end':  30
            }.
            {
                'start': 50,
                'end': 60
            }
        ]
    '''
    pages = []
    for part in range_str.split(','):
        if '-' in part:
            [start, end] = part.split('-')
            pages.append({
                'start': int(start), 
                'end': int(end)
            })
        else:
            pages.add({
                'start': int(part),
                'end': int(part) + 1
            })

    return sorted(pages, key = lambda obj: obj['start'])


def main():
    parser = argparse.ArgumentParser(description="Process a PDF file input.")
    parser.add_argument("file", type=argparse.FileType('rb'), help="Path to the input PDF file")
    parser.add_argument(
        "--range",
        type=str,
        help="Range of pages to process (e.g., '1-3,5,7-9')",
        default=None
    )

    args = parser.parse_args()

    file_handler = args.file

    pdf_pages = parse_pdf(file_handler)



    if args.range:
        selected_pages = parse_page_range(args.range)
        partial_list_pdf_pages = []

        for range in selected_pages:
            start = range['start']
            end = range['end']
            partial_list_pdf_pages += pdf_pages[start : end]

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
