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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        node_text = node.text
        image_list = extract_markdown_images(node_text)

        # handle string with no images
        if image_list == []:
            new_nodes.append(node)
        
        # repeatedly split text and add TextNodes to new_nodes
        current_text = node_text
        for (alt, url) in image_list:
            current_image_markdown = f"![{alt}]({url})"
            before, after = current_text.split(current_image_markdown, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.PLAIN))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = after
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        node_text = node.text
        link_list = extract_markdown_links(node_text)

        # handle string with no links
        if link_list == []:
            new_nodes.append(node)
        
        # repeatedly split text and add TextNodes to new_nodes
        current_text = node_text
        for (text, url) in link_list:
            current_text_markdown = f"[{text}]({url})"
            before, after = current_text.split(current_text_markdown, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.PLAIN))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            current_text = after
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.PLAIN))

    return new_nodes