#This file is used to create the file controller for webots. It ment to be run as a compiler file. When you chenge anythin on the source code you
#have to run this script to update the WebotsCOntroller file wich is ment to be load as the controller in Erebus platform.

import os
# def read_file(file_path):
#     """Return the contnent of a file as a forated oneline string"""
#     try:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             modified_content = '\\\n'.join(line.strip() for line in lines)
#             return modified_content
#     except FileNotFoundError:
#         return f"{src_folder}/{file_path} not found"
#     except Exception as e:
#         return f"Error reading the file: {str(e)}"
import black

def read_file(input_file):
    try:
        # Read the content of the input Python file
        with open(input_file, 'r') as file:
            python_code = file.read()

        # Format the Python code using black
        formatted_code = black.format_file_contents(python_code, fast=False, mode=black.Mode())

        # Remove newlines to make it a single-line string
        formatted_code = formatted_code.replace('\n', '\\n')

        return formatted_code
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



ALL_FOLDER_FILES = []
def check_dir(dir):
    """Add to ALL_FOLDER_FILES all the file's paths that the folder has"""
    contents = os.listdir(dir)
    files = [f for f in contents if os.path.isfile(os.path.join(dir, f))]
    folders = [d for d in contents if os.path.isdir(os.path.join(dir, d))]

    for file in files:
        ALL_FOLDER_FILES.append(f"{dir}/{file}")
    
    for folder in folders:
        if folder != "__pycache__":
            check_dir(f"{dir}/{folder}")
    


base_code_file = "scripts/basecontroller.txt"
src_folder = "src"  
insert_modules=False
check_dir(src_folder)

content = ""
with open("scripts/basecontroller.txt", "r") as base_code:
    for line in base_code.readlines():
        if line.strip() == "#INSERT_MODULES":
            insert_modules = True
        elif insert_modules:
            for file in ALL_FOLDER_FILES:
                file_content=read_file(file).replace('"',"'")

                path_parts = file.split("/")
                path_parts.pop(0)
                new_path = "/".join(path_parts)
                content += f'    __stickytape_write_module("{new_path}",b"{file_content}")\n'
            insert_modules = False  # Disable module insertion after processing
        else:
            content += line
    

with open("WeebotsController.py", "w") as code:
    code.write(content)
