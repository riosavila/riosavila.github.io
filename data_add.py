import re
import io

def process_file(input_file, output_file):
    # Try different encodings
    encodings = ['utf-8', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with io.open(input_file, 'r', encoding=encoding) as f:
                content = f.read()
            break  # If successful, exit the loop
        except UnicodeDecodeError:
            continue  # If unsuccessful, try the next encoding
    else:
        raise ValueError(f"Unable to decode the file with any of these encodings: {encodings}")

    # Split the content into sections based on the "##" headings
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)

    processed_content = []
    for section in sections:
        if section.strip():
            # Extract the heading (dataset name)
            match = re.match(r'^## (.+)$', section, re.MULTILINE)
            if match:
                dataset_name = match.group(1).strip()
                
                # Add the callout note at the end of the section
                callout = f"\n\n:::{{\\.callout-note}}  \n## AI Description \n{{{{< include datades/{dataset_name}.ddes >}}}}\n:::"
                processed_section = section + callout
                processed_content.append(processed_section)
            else:
                processed_content.append(section)

    # Write the processed content to the output file
    with io.open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_content))

# Usage
input_file = 'sdata.qmd'
output_file = 'sdata2.qmd'
process_file(input_file, output_file)