import tkinter as tk
import openai
import pytesseract
from PIL import Image, ImageTk
import tkinter.filedialog
import fitz  # PyMuPDF

# Replace the value of `API_KEY` with your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# GUI
root = tk.Tk()
root.title("Essay Grader")

frame = tk.Frame(root)
frame.pack(pady=10)

def ocr_pdf(file_path):
    # Use PyMuPDF (fitz) to extract text from PDF
    pdf_document = fitz.open(file_path)
    pdf_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pdf_text += page.get_text()
    return pdf_text

def convert_pdf_to_image(file_path):
    # Use PyMuPDF (fitz) to convert the first page of PDF to an image
    pdf_document = fitz.open(file_path)
    page = pdf_document.load_page(0)
    image = page.get_pixmap()
    image_path = "pdf_image.png"
    image.save(image_path)
    return image_path

def grade_essay_from_image():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[('Image files', '*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm'), ('All files', '*.*')])
    if file_path:
        img = Image.open(file_path)

        # Run OCR on the image
        essay_text = pytesseract.image_to_string(img)

        # Send the extracted essay to OpenAI's GPT-4 for grading
        model_engine = "gpt-3.5-turbo-16k-0613"
        prompt = f"Grade this essay on a scale of band 1 to 9 based on IELTS Scoring Method: {essay_text}\n\nComments:"

        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "You are an essay grader."},
                {"role": "user", "content": prompt},
            ],
        )

        feedback = response['choices'][0]['message']['content']
        display_image_and_summary(file_path, essay_text, feedback)

def grade_essay_from_pdf():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
    if file_path:
        essay_text = ocr_pdf(file_path)

        # Send the extracted essay to OpenAI's GPT-4 for grading
        model_engine = "gpt-3.5-turbo-16k-0613"
        prompt = f"Grade this essay on a scale of band 1 to 9 based on IELTS Scoring Method: {essay_text}\n\nComments:"

        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "You are an essay grader."},
                {"role": "user", "content": prompt},
            ],
        )

        feedback = response['choices'][0]['message']['content']
        image_path = convert_pdf_to_image(file_path)
        display_image_and_summary(image_path, essay_text, feedback)

def clear_all():
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

def display_image_and_summary(file_path, ocr_content, feedback):
    global content_label, summary_label
    if 'content_label' in globals():
        content_label.destroy()
    if 'summary_label' in globals():
        summary_label.destroy()

    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ppm', '.pgm')):
        img = Image.open(file_path)
        img = img.resize((img.width // 2, img.height // 2), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=image)
        image_label.image = image
        image_label.pack(side=tk.LEFT, padx=10)
    elif file_path.lower().endswith('.pdf'):
        img = Image.open(file_path)
        img = img.resize((img.width // 2, img.height // 2), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame, image=image)
        image_label.image = image
        image_label.pack(side=tk.LEFT)

    # Display only the feedback and exclude OCR text
    summary_label = tk.Label(frame, text=feedback, font=("TkDefaultFont", 12), wraplength=500)
    summary_label.pack(side=tk.LEFT)

# Button for selecting an image and grading the essay
select_image_button = tk.Button(frame, text="Select Image and Grade Essay", command=grade_essay_from_image)
select_image_button.pack(pady=10)

# Button for selecting a PDF and grading the essay
select_pdf_button = tk.Button(frame, text="Select PDF and Grade Essay", command=grade_essay_from_pdf)
select_pdf_button.pack(pady=10)

# Button for clearing the displayed content
clear_all_button = tk.Button(frame, text="Clear All", command=clear_all)
clear_all_button.pack(pady=10)

root.mainloop()