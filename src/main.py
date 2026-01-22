#!/usr/bin/env python

import textnode as tn
from page_functions import *

def main():
    print("Hello from static-site-generator!")
    copy_contents_to_destination(
        "static", 
        "public", 
        "public"
        )
    generate_pages_recursive(
        "content", 
        "template.html", 
        "public"
        )

if __name__ == "__main__":
    main()
