import json

# Input and output file names
input_file = "metamask.json"  # Replace with your actual JSON file name
output_file = "extracted_messages.txt"

# Load JSON data from file
with open(input_file, "r", encoding="utf-8") as file:
    try:
        data = json.load(file)  # Try to load JSON properly
        if isinstance(data, str):  # If JSON is wrapped in a string, parse again
            data = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

# Extract only author and text from the mapping field
output_lines = []
mapping = data.get("mapping", {})  # Get the mapping dictionary

for key, value in mapping.items():
    if not isinstance(value, dict):  # Skip if value isn't a dictionary
        print(f"Skipping key {key} due to unexpected structure.")
        continue

    message = value.get("message", {})
    if not message:  # Skip if message is missing
        continue

    author = message.get("author", {}).get("role", "unknown")
    text_parts = message.get("content", {}).get("parts", [])

    texts = [part for part in text_parts if isinstance(part, str)]  # Ensure it's a string

    if texts:
        output_lines.append(f"Author: {author}\nText: {' '.join(texts)}\n{'-'*40}\n")

# Save to a text file
if output_lines:
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(output_lines)
    print(f"Data extracted and saved to {output_file}")
else:
    print("No messages found with author and text.")
