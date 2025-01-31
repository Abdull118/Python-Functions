import os
import subprocess

# Folder containing PowerPoint files
ppt_folder = "/Users/arashnaimi/Library/Mobile Documents/com~apple~CloudDocs/TouroCOM/Year 2/Semester 2/OMM/Exam 1/OMM 4 - Spring - Exam 1"
output_folder = "/Users/arashnaimi/Library/Mobile Documents/com~apple~CloudDocs/TouroCOM/Year 2/Semester 2/OMM/Exam 1/OMM 4 - Spring - Exam 1"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Convert each PowerPoint file to PDF
for file in os.listdir(ppt_folder):
    if file.endswith(".pptx") or file.endswith(".ppt"):
        input_path = os.path.join(ppt_folder, file)
        output_path = os.path.join(output_folder, file.rsplit(".", 1)[0] + ".pdf")
        
        # Run LibreOffice command-line conversion
        subprocess.run([
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            "--headless", "--convert-to", "pdf", input_path, "--outdir", output_folder
        ])

print("Conversion complete!")
