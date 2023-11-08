# AutoGrader-GPT



https://github.com/zawawiAI/AutoGrader-GPT/assets/50743060/e0e4d989-5b0b-48a2-ba2a-a8989579480b





This is a simple Python application for grading essays based on the IELTS Scoring Method using OpenAI's GPT-3.5 Turbo model. The application allows you to grade essays from both image files and PDF documents.
Prerequisites

Before running the application, make sure you have the required Python libraries installed. You can install them using the following commands:

bash

pip install tkinter openai pytesseract pillow PyMuPDF

Setup

You will need to replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key.

python

openai.api_key = 'YOUR_OPENAI_API_KEY'

Usage

    Run the application by executing the Python script.

bash

python essay_grader.py

    The main window will appear with the following options:

    Select Image and Grade Essay: Click this button to select an image (e.g., a scanned essay) for grading.
    Select PDF and Grade Essay: Click this button to select a PDF document for grading.
    Clear All: Click this button to clear the displayed content.

    After selecting an image or PDF, the application will extract the text using OCR (Optical Character Recognition) and send it to the OpenAI GPT-3.5 Turbo model for grading.

    The grading result and feedback will be displayed on the application window.

Note

    The OCR functionality uses the PyMuPDF library to extract text from PDF documents.
    The grading is done based on the IELTS Scoring Method.

Disclaimer

This application is a simple demonstration of how to use OpenAI's GPT-3.5 Turbo for grading essays. The accuracy of the grading may vary, and it is intended for educational purposes.
