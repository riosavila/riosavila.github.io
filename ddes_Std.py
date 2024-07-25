import os
import re

def extract_research_ideas(content):
    # Find the "Potential research ideas" section
    match = re.search(r'3\.\s*Potential research ideas:(.*?)($|\n\d+\.)', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def standardize_research_ideas(ideas):
    # Split ideas into a list
    idea_list = re.split(r'\n\s*[-a-z\d)]\.?\s*', ideas)
    idea_list = [idea.strip() for idea in idea_list if idea.strip()]
    
    # Format ideas
    formatted_ideas = "3. Potential research ideas:\n\n"
    for i, idea in enumerate(idea_list, 1):
        formatted_ideas += f"   {i}. {idea}\n\n"
    
    return formatted_ideas.strip()

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract and standardize research ideas
    research_ideas = extract_research_ideas(content)
    standardized_ideas = standardize_research_ideas(research_ideas)
    
    # Replace the original research ideas section with the standardized one
    new_content = re.sub(
        r'3\.\s*Potential research ideas:.*?($|\n\d+\.)',
        standardized_ideas + '\n',
        content,
        flags=re.DOTALL
    )
    
    return new_content

def process_folder(folder_path):
    # Get all .ddes files in the folder
    ddes_files = [f for f in os.listdir(folder_path) if f.endswith('.ddes')]
    
    if not ddes_files:
        print("No .ddes files found in the specified folder.")
        return
    
    # Process each file
    for file_name in ddes_files:
        file_path = os.path.join(folder_path, file_name)
        standardized_content = process_file(file_path)
        
        # Write the standardized content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(standardized_content)
        
        print(f"Processed: {file_name}")


# Usage
folder_path = "datades2"  # Replace with the actual path to your folder
process_folder(folder_path)