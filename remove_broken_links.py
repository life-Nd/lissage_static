import os
import re
import json

def find_and_replace_broken_links(root_dir):
    broken_links = []

    # Updated regular expression to match all specified patterns
    pattern = re.compile(r'(?:href|src|concatemoji)=[\'"]((?:/wp-(?:content|includes)/[^\'"]+\.(?:css|js|min\.css|min\.js))[^\'"]*(?:\?ver=[^\'"]+)?)[\'"]')

    # Loop through all files in the directory
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith((".html", ".php", ".css", ".js")):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                modified_content = content
                modified = False

                # Find all matches
                matches = pattern.findall(content)
                for match in matches:
                    clean_path = match.split("?")[0]
                    full_path = os.path.normpath(os.path.join(root_dir, clean_path.lstrip('/')))
                    
                    if not os.path.exists(full_path):
                        broken_links.append({
                            "file": file_path,
                            "link": match,
                            "line": get_line_number(content, match)
                        })
                    
                    # Replace the full match with the clean path
                    modified_content = modified_content.replace(match, clean_path)
                    modified = True

                # If any modification was made, write the new content back to the file
                # if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

    return broken_links

def get_line_number(content, match):
    """Returns the line number where the match was found"""
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        if match in line:
            return i
    return None

def main():
    root_directory = "/Users/lifen/Downloads/mariana-lissage_simply_static"
    broken_links = find_and_replace_broken_links(root_directory)
    print(f"{len(broken_links)} broken links found and fixed.")
    
    # Save the broken links to a JSON file
    with open('broken_links.json', 'w', encoding='utf-8') as json_file:
        json.dump(broken_links, json_file, indent=4)

if __name__ == "__main__":
    main()