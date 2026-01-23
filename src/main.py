#!/usr/bin/env python

import sys
from page_functions import *

def main():
    print("Hello from static-site-generator!")
    if sys.argv:
        basepath = sys.argv[0] #.split("/")[0]
    else:
        basepath = "/"
    copy_contents_to_destination(
        "static", 
        "public", 
        "public"
        )
    generate_pages_recursive(
        "content", 
        "template.html", 
        "public", basepath
        )

if __name__ == "__main__":
    main()
