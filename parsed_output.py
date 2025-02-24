import json
import re

def parse_faq(text):
    faq_list = []
    
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
            print(f"{pair['question']}|{pair['answer']}")

# Sample input text
with open("anki_flash_card_llama3.2.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Parsing the text
parse_faq(text)

