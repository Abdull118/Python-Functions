import re

# Input and output file paths
input_file_path = './extracted_pdf_content.txt'
output_file_path = './extracted_rationales.txt'

def extract_rationales_from_text(file_path):
    """
    Extract rationale text and corresponding numbers from the provided text file.
    :param file_path: Path to the text file containing extracted content
    :return: A sorted list of tuples with number and rationale
    """
    rationales = []

    # Read the content of the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        full_text = file.read()

    # Regular expression to match numbers (e.g., 69> or 68X) and rationale
    pattern = r"(\d+)[X>]\s.*?Rationale:\s*(.+?)(?=Learning Outcomes|(?:\d+[X>]|$))"

    # Search for all matches in the text
    matches = re.finditer(pattern, full_text, re.DOTALL)
    for match in matches:
        number = int(match.group(1))  # Extract and convert the number to an integer
        rationale = match.group(2).strip()  # Extract the rationale text
        rationales.append((number, rationale))

    # Sort the rationales by numeric value of the question number
    rationales.sort(key=lambda x: x[0])

    return rationales

# Extract rationales from the text file
rationales = extract_rationales_from_text(input_file_path)

# Save the extracted rationales to a new text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for number, rationale in rationales:
        output_file.write(f"{number}: {rationale}\n\n")

print(f"Extracted rationales have been saved to {output_file_path}")
