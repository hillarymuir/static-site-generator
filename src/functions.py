#!/usr/bin/env python

#TODO: refactor to split into multiple files

import re

from htmlnode import LeafNode, HTMLNode, ParentNode
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

# helper functions and markdown_to_html_node

# helper function that takes text and returns a list of LeafNodes
def text_to_children(text):
    children = []

    textnodes = text_to_textnodes(text)

    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))

    return children

# helper functions to transform blocks into html nodes based on their types
def paragraph_block_to_html_node(block):
    # replace newlines with spaces
    corrected_block = block.replace("\n", " ")

    # convert block to children and create parent node
    children = text_to_children(corrected_block)
    parent_node = ParentNode("p", children)
    return parent_node

def heading_block_to_html_node(block):
    # count octothorpes to determine heading number
    heading_num = block.count("#", 0, block.find(" "))
    tag = f"h{heading_num}"

    # remove octothorpes from block
    corrected_block = block[heading_num+1:]

    # convert block to children and create parent node
    children = text_to_children(corrected_block)
    parent_node = ParentNode(tag, children)
    return parent_node

def code_block_to_html_node(block):
    # remove backticks from block
    corrected_block = block[4:-4]

    # code block node does not process internal tags
    inner_node = LeafNode("code", corrected_block)
    return ParentNode("pre", [inner_node])

def quote_block_to_html_node(block):
    # remove >s from block
    corrected_block = block[2:].replace("\n> ", "\n")

    # convert block to children and create parent node
    children = text_to_children(corrected_block)
    parent_node = ParentNode("blockquote", children)
    return parent_node

def unordered_list_to_html_node(block):
    line_children = []

    line_list = block[2:].split("\n- ")
    for line in line_list:
        # convert lines to child nodes and add to list of line children
        inner_nodes = text_to_children(line)
        line_children.append(ParentNode("li", inner_nodes))

    parent_node = ParentNode("ul", line_children)
    return parent_node

def ordered_list_to_html_node(block):
    line_children = []

    line_list = re.split(r"\n\d. ", block[3:])
    for line in line_list:
        # convert lines to child nodes and add to list of line children
        inner_nodes = text_to_children(line)
        line_children.append(ParentNode("li", inner_nodes))

    parent_node = ParentNode("ol", line_children)
    return parent_node

def markdown_to_html_node(md):
    high_lvl_children = []
    md_blocks = markdown_to_blocks(md)

    for block in md_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                high_lvl_children.append(paragraph_block_to_html_node(block))
            case BlockType.HEADING:
                high_lvl_children.append(heading_block_to_html_node(block))
            case BlockType.CODE:
                high_lvl_children.append(code_block_to_html_node(block))
            case BlockType.QUOTE:
                high_lvl_children.append(quote_block_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                high_lvl_children.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                high_lvl_children.append(ordered_list_to_html_node(block))
            case _:
                raise ValueError("Error: invalid BlockType")

    parent_node = ParentNode("div", high_lvl_children)
    return parent_node

def extract_title(markdown):
    block_list = markdown_to_blocks(markdown)

    for block in block_list:
        if block.startswith("# "):
            return block[2:]
    
    raise Exception("Error: no h1 header")