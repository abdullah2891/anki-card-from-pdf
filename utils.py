import re
import PyPDF2
from typing import Generator, List, Dict
from data.anki_card_prompt import anki_card_prompt


def parse_answer_question(text):
    faq_list = []
    formatted_output = ""

    if not isinstance(text, str):
        return ""

    # Removing separator lines
    text = re.sub(r"\n\+{10,}\n", "\n", text)

    # Extracting Q&A pairs
    qa_pairs = re.findall(r"Q:\s*(.*?)\nA:\s*(.*?)(?=\nQ:|\Z)", text, re.DOTALL)
    for question, answer in qa_pairs:
        faq_list.append({"question": question.strip(), "answer": answer.strip()})

    # Extracting bullet point Q&A format
    bullet_qa = re.findall(r"\u2022(.*?)\n(.*?)(?=\n\u2022|\Z)", text, re.DOTALL)
    for question, answer in bullet_qa:
        faq_list.append({"question": question.strip(), "answer": answer.strip()})

    # Extracting simple question-answer pairs
    line_qa = re.findall(r"(.*?)\?\s*(.*?)(?=\n[A-Z]|\Z)", text, re.DOTALL)
    for question, answer in line_qa:
        faq_list.append({"question": question.strip() + "?", "answer": answer.strip()})

    for pair in faq_list:
        if bool(pair["question"]) and bool(pair["answer"]):
            formatted_output += f"{pair['question']}|{pair['answer']}" + "\n"

    return formatted_output


def generate_prompt(prompot_dict, data) -> str:
    """
    helps to build effective prompt
    """
    goal = prompot_dict["goal"]
    return_format = prompot_dict["return_format"]
    warnings = prompot_dict["warnings"]

    return f" \n {goal} \n {return_format} \n {warnings} \n {data}"


def parse_pdf(fh) -> Generator:
    with fh as f:
        reader = PyPDF2.PdfReader(f)
        return [
            generate_prompt(anki_card_prompt, page.extract_text())
            for page in reader.pages
            if page.extract_text()
        ]


def parse_page_range(range_str: str) -> List[Dict[str, int]]:
    """
    returns list start and end list
    [
        {
            'start': 20,
            'end':  30
        },
        {
            'start': 50,
            'end': 60
        }
    ]
    """
    pages = []
    for part in range_str.split(","):
        if "-" in part:
            try:
                start, end = map(int, part.split("-"))
                pages.append({"start": start, "end": end})
            except ValueError:
                raise ValueError(
                    f"Invalid range format: {part}. Start and end must be integers."
                )
        else:
            try:
                page = int(part)
                pages.append({"start": page, "end": page + 1})
            except ValueError:
                raise ValueError(f"Invalid page number: {part}. Must be an integer.")

    return sorted(pages, key=lambda obj: obj["start"])
