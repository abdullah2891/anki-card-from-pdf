# README
================

Table of Contents
-----------------

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Usage](#usage)
4. [Known Issues](#known-issues)

Introduction
------------

This project is designed to parse PDF files and generate effective prompts for a Large Language Model (LLM). The script uses the PyPDF2 library to extract text from the input PDF, and then applies a series of natural language processing (NLP) transformations to create prompts.

Requirements
------------

* Python 3.8+
* PyPDF2 library (`pip install PyPDF2`)
* Argparse library (`pip install argparse`)
* Multiprocessing library (`pip install multiprocessing`)

Usage
-----

1. Save this script as `pdf_prompt_generator.py`.
2. Run the script using the following command: `python pdf_prompt_generator.py <input_pdf_file>`
3. The script will generate prompts for each page in the input PDF and print them to the console.

Known Issues
------------

* This script assumes that the input PDF contains text that can be parsed by the PyPDF2 library.
* If the input PDF is corrupted or does not contain any readable text, the script may fail.
* The use of multiple processes to generate prompts simultaneously may lead to issues if the system resources are insufficient.

Code Explanation
-----------------

The code is organized into several functions:

1. `parse_answer_question`: takes a string input and extracts relevant Q&A pairs from it.
2. `generate_prompt`: generates effective prompts based on user-defined parameters.
3. `run_llm_model`: runs an LLM model with the generated prompt as input.
4. `parse_pdf`: parses a PDF file using PyPDF2 and extracts text from each page.

The main function uses argparse to parse command-line arguments, and then calls the `parse_pdf` function to extract text from the input PDF. The extracted text is then passed through the `generate_prompt` function to create effective prompts, which are finally generated by the `run_llm_model` function using an LLM model.

License
-------

This script is released under the MIT License.

MIT License

Copyright (c) [Year] [Author]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

