#!/usr/bin/env python

import textnode as tn
from page_functions import *

def main():
    print("Hello from static-site-generator!")
    copy_contents_to_destination("static", "public", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
