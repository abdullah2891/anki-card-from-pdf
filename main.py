from typing import Generator
import argparse
import PyPDF2
from data.anki_card_prompt import anki_card_prompt
import subprocess


def generate_prompt(prompot_dict: dict) -> str:
    '''
    helps to build effective prompt

    '''
    goal = prompot_dict['goal']
    return_format = prompot_dict['return_format']
    warnings = prompot_dict['warnings']


    return f" \n {goal} \n {return_format} \n {warnings}" 


def run_llm_model(prompt: str) -> str:
    
    # Command to run with shell features (e.g., command substitution)
    command = f'ollama run llama3.2 "{prompt}"'

    # Execute the command, capturing the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check if the command ran successfully
    if result.returncode == 0:
        print("Command output:")
        return result.stdout
    else:
        raise ValueError(result.stderr)



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
    prompt = generate_prompt(anki_card_prompt)
    generate = run_llm_model(prompt)
    print(generate)

