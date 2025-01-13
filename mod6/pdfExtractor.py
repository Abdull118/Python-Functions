import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Set the path to Tesseract OCR if needed (uncomment if necessary)
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

file_path = './pdf/15.pdf'
output_file_path = './txt/cs15.txt'

# Extract text using PyPDF2 and fall back to OCR for image-based content
with open(file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = []

    # Extract text from each page using PyPDF2
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
        else:
            # Use OCR if PyPDF2 extraction fails
            print(f"Page {i + 1} has image content. Extracting with OCR...")
            images = convert_from_path(file_path, first_page=i + 1, last_page=i + 1)
            for image in images:
                ocr_text = pytesseract.image_to_string(image)
                text.append(ocr_text)

# Combine all extracted text into a single string
full_text = '\n\n'.join(text)

# Save the extracted content to a text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(full_text)

print(f"Extracted content has been saved to {output_file_path}")
