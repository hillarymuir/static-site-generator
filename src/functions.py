#!/usr/bin/env python

import re

from htmlnode import LeafNode
from textnode import TextType, TextNode

def text_node_to_html_node(text_node):
    # handle text type, convert to tag
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {
                    "src": text_node.url,
                    "alt": text_node.text
                }
            )
        case _:
            raise ValueError("Error: TextNode type is invalid")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # note: assumes delimiter will match text_type
    new_nodes = []

    for node in old_nodes:
        # check for orphan delimiters
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Odd number of {text_type} delimiters")

        # split text at delimiter and set text type of each segment based on whether even or odd
        split_text = node.text.split(sep=delimiter)
        for i, text_segment in enumerate(split_text):
            if i == 0 or i % 2 == 0:
                new_nodes.extend([TextNode(text_segment, TextType.PLAIN)])
            else:
                new_nodes.extend([TextNode(text_segment, text_type)])

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches