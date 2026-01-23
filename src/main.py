#!/usr/bin/env python

import sys
from page_functions import *

def main():
    print("Hello from static-site-generator!")
    if sys.argv:
        basepath = sys.argv[1] + "/"
    else:
        basepath = "/"
    copy_contents_to_destination(
        "static", 
        "docs", 
        "docs"
        )
    generate_pages_recursive(
        "content", 
        "template.html", 
        "docs", basepath
        )

if __name__ == "__main__":
    main()
