#!/usr/bin/env python

#TODO: refactor to split into multiple files

import re

from htmlnode import LeafNode
from textnode import TextType, TextNode
from blocktype import BlockType

# inline markdown

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
                new_nodes.extend([TextNode(text_segment, node.text_type)])
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
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue # ignore text that is not plain; nested tag functionality to be added

        node_text = node.text
        image_list = extract_markdown_images(node_text)
        
        # repeatedly split text and add TextNodes to new_nodes
        current_text = node_text
        for (alt, url) in image_list:
            current_image_markdown = f"![{alt}]({url})"
            before, after = current_text.split(current_image_markdown, 1)
            if before:
                new_nodes.append(TextNode(before, node.text_type))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = after
        if current_text:
            new_nodes.append(TextNode(current_text, node.text_type))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue # ignore text that is not plain; nested tag functionality to be added
        node_text = node.text
        link_list = extract_markdown_links(node_text)
        
        # repeatedly split text and add TextNodes to new_nodes
        current_text = node_text
        for (text, url) in link_list:
            current_text_markdown = f"[{text}]({url})"
            before, after = current_text.split(current_text_markdown, 1)
            if before:
                new_nodes.append(TextNode(before, node.text_type))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            current_text = after
        if current_text:
            new_nodes.append(TextNode(current_text, node.text_type))

    return new_nodes

def text_to_textnodes(text):
    starting_textnode = [TextNode(text, TextType.PLAIN)]
    b_textnodes = split_nodes_delimiter(starting_textnode, "**", TextType.BOLD)
    b_i_textnodes = split_nodes_delimiter(b_textnodes, "_", TextType.ITALIC)
    b_i_c_textnodes = split_nodes_delimiter(b_i_textnodes, "`", TextType.CODE)
    b_i_c_img_textnodes = split_nodes_image(b_i_c_textnodes)
    b_i_c_img_link_textnodes = split_nodes_link(b_i_c_img_textnodes)
    return b_i_c_img_link_textnodes

# block markdown
def markdown_to_blocks(md):
    block_list = md.split("\n\n")
    for i, block in enumerate(block_list):
        block_list[i] = block.strip()
        if block == "":
            del block_list[i]
    return block_list

def block_to_block_type(block):

    # check for the easy ones (heading and code)
    heading_list = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    if block.startswith(tuple(heading_list)):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # assume each type of line-by-line blocktype is true, then try to disprove each one
    is_quote = True
    is_unordered_list = True
    is_ordered_list = True
    ordered_list_correct_line = 1
    line_list = block.split("\n")
    for line in line_list:
        if not line.startswith("> "):
            is_quote = False
        if not line.startswith("- "):
            is_unordered_list = False
        if not line.startswith(f"{ordered_list_correct_line}. "):
            is_ordered_list = False
        ordered_list_correct_line += 1

    # check if any of the line-by-line blocktypes have not been disproven
    if is_quote:
        return BlockType.QUOTE
    elif is_unordered_list:
        return BlockType.UNORDERED_LIST
    elif is_ordered_list:
        return BlockType.ORDERED_LIST

    # return default if no other blocktypes found
    return BlockType.PARAGRAPH