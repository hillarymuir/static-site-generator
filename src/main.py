#!/usr/bin/env python

import textnode as tn

def main():
    print("Hello from static-site-generator!")

    test_textnode = tn.TextNode(
        "This is some anchor text", "link", "https://www.boot.dev"
        )
    print(test_textnode)


if __name__ == "__main__":
    main()
