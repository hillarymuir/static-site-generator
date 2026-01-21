#!/usr/bin/env python

import os
import shutil
import textnode as tn

def copy_contents_to_destination(source_dir, destination_dir):
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

    # delete contents of destination
    shutil.rmtree(destination_dir)
    os.mkdir("/home/hillary/static-site-generator/src/public")

    # TODO copy all files, subdirectories, and nested files

    # TODO log path of each copied file for debugging


def main():
    print("Hello from static-site-generator!")

    print("Testing emptying of public...")
    copy_contents_to_destination("src/static", "src/public")


if __name__ == "__main__":
    main()
