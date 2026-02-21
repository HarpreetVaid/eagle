import os
import shutil
import re

# IMPORTANT: Make sure this is running in the root directory
# We're transforming: 
# "eagle" -> "eagle"
# "Eagle" -> "Eagle"
# "EAGLE" -> "EAGLE"

ROOT_DIR = "/mnt/c/Users/harpr/Downloads/AI-project/eagle"

def get_replacements(text):
    text = text.replace("eagle", "eagle")
    text = text.replace("Eagle", "Eagle")
    text = text.replace("EAGLE", "EAGLE")
    return text

def process_file_content(filepath):
    # Try reading as utf-8, if it fails, it might be a binary file like pdf/png
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        return False
        
    new_content = get_replacements(content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def rename_recursive(path):
    # Process files bottom-up so renaming a dir doesn't break inner paths
    for root, dirs, files in os.walk(path, topdown=False):
        
        # Skip git
        if ".git" in root:
            continue
            
        for name in files:
            # 1. Process Content
            filepath = os.path.join(root, name)
            if process_file_content(filepath):
                print(f"Updated content: {filepath}")
                
            # 2. Rename File
            new_name = get_replacements(name)
            if new_name != name:
                new_filepath = os.path.join(root, new_name)
                os.rename(filepath, new_filepath)
                print(f"Renamed file: {filepath} -> {new_name}")
                
        for name in dirs:
            # 3. Rename Directory
            new_name = get_replacements(name)
            if new_name != name:
                dirpath = os.path.join(root, name)
                new_dirpath = os.path.join(root, new_name)
                os.rename(dirpath, new_dirpath)
                print(f"Renamed dir: {dirpath} -> {new_name}")

if __name__ == "__main__":
    
    # 1. Rename everything inside the directory
    print("Starting deep rename...")
    rename_recursive(ROOT_DIR)
    print("Renaming complete!")
    
    # 2. Finally rename the top-level directory root itself
    parent_dir = os.path.dirname(ROOT_DIR)
    new_root_dir = os.path.join(parent_dir, "eagle")
    
    # If the root dir doesn't already contain "eagle"
    if ROOT_DIR != new_root_dir:
        os.rename(ROOT_DIR, new_root_dir)
        print(f"Renamed root: {ROOT_DIR} -> {new_root_dir}")
