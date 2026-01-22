#!/usr/bin/env python

import os
import shutil
import textnode as tn

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


def main():
    print("Hello from static-site-generator!")
    copy_contents_to_destination("static", "src/public", "src/public")


if __name__ == "__main__":
    main()
