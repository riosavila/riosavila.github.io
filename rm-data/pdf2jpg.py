# Step 1: Install necessary libraries
# Run these commands in your terminal
# pip install pdf2image
# pip install pillow

# Step 2: Import necessary libraries
from pdf2image import convert_from_path
from PIL import Image
import os

# Step 3: Define the function to convert PDF to JPG
def pdf_to_jpg(pdf_path, output_folder):
    """
    Convert PDF pages to JPG images.

    Parameters:
    pdf_path (str): The path to the PDF file.
    output_folder (str): The folder to save the JPG images.

    Returns:
    None
    """
    # Step 4: Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Step 5: Save each image as a JPG file
    for i, image in enumerate(images):
        jpg_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        image.save(jpg_path, 'JPEG')
        print(f"Saved {jpg_path}")

# Example usage
pdf_path = "case_study_returns.pdf"  # Path to your PDF file
output_folder = "output_images"  # Folder to save JPG images
pdf_to_jpg(pdf_path, output_folder)