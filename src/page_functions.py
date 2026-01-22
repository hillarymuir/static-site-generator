#!/usr/bin/env python

import os
import shutil
from functions import markdown_to_html_node, extract_title

def copy_contents_to_destination(source_dir, destination_dir, parent):
    # ensure paths exist and convert to absolute paths if relative paths were input
    if not os.path.exists(source_dir):
        try:
            source_dir = f"{os.path.abspath(source_dir)}"
        except [ValueError]:
            print("Error: source directory path does not exist")
    elif not os.path.exists(destination_dir):
        try:
            destination_dir = f"{os.path.abspath(destination_dir)}"
        except [ValueError]:
            print("Error: destination directory does not exist")
    elif not os.path.exists(parent):
        try:
            destination_dir = f"{os.path.abspath(parent)}"
        except [ValueError]:
            print("Error: parent directory does not exist")


    # delete contents of destination if it is public so there is a fresh slate
    if destination_dir == parent:
        shutil.rmtree(parent)
        os.mkdir(parent)

    # copy all files, subdirectories, and nested files
    for entry in os.listdir(source_dir):
        entry_path = os.path.join(source_dir, entry)
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, destination_dir)
            log_path = os.path.abspath("copy_log.txt")
            with open(log_path, "a") as f:
                f.write(f"Copying {entry_path} to {destination_dir}\n")
        else:
            new_destination_path = os.path.join(destination_dir, entry)
            os.mkdir(new_destination_path)
            copy_contents_to_destination(entry_path, new_destination_path, parent)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    from_file_contents = f.read()
    f.close()

    f = open(template_path)
    template_file_contents = f.read()
    f.close()

    from_file_html_str = markdown_to_html_node(from_file_contents).to_html()
    page_title = extract_title(from_file_contents)

    file_with_title = template_file_contents.replace("{{ Title }}", page_title)
    file_with_title_and_content = file_with_title.replace("{{ Content }}", from_file_html_str)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w+") as f:
        f.write(file_with_title_and_content)