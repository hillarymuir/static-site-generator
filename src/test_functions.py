#!/usr/bin/env python

import unittest
from functions import *
from textnode import TextNode, TextType

class TestFunctions(unittest.TestCase):

    # text_node_to_html_node tests

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://boot.dev",
            "alt": "This is an image node"
            })
        
    # split_notes_delimiter tests
    def test_bold_split(self):
        node = TextNode("This is text with a **bold** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.PLAIN),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word", TextType.PLAIN),
                        ])
    
    def test_italic_split(self):
        node = TextNode("This is text with an _italic_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with an ", TextType.PLAIN),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word", TextType.PLAIN),
                        ])
        
    def test_code_split(self):
        node = TextNode("This is text with a `code block` in it", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.PLAIN),
                            TextNode("code block", TextType.CODE),
                            TextNode(" in it", TextType.PLAIN),
                        ])
        
    def test_hanging_asterisks(self):
        node = TextNode("This is text with naughty unpaired **asterisks", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_hanging_underscore(self):
        node = TextNode("This is text with an under_score without a friend", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_hanging_backtick(self):
        node = TextNode("This is text with a `lonely backtick", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_initial_italic(self):
        node = TextNode("_This_ is text with an italic word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
                         [
                            TextNode("", TextType.PLAIN),
                            TextNode("This", TextType.ITALIC),
                            TextNode(" is text with an italic word", TextType.PLAIN),
                        ])
        
    # test extraction of markdown images and links
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),
                              ("to youtube", "https://www.youtube.com/@bootdotdev")],
                              matches)
    # add more edge cases here

    # test splitting of image and link strings into TextNodes
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "There are no images here",
            TextType.PLAIN
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("There are no images here", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
            "There are no links here",
            TextType.PLAIN
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("There are no links here", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    # tests for text_to_textnodes

    def test_text_to_textnodes_all_modifiers(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_no_modifiers(self):
        text = "This is text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([
                TextNode("This is text", TextType.PLAIN)
            ],
            new_nodes,
        )

    # markdown to blocks tests
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_heading_block(self):
        md = """
# This is a heading
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading"
            ],
        )

    
    def test_markdown_to_block_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    # block to block type
    def test_block_to_block_type_para(self):
        block = "This is a paragraph."
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_h1(self):
        block = "# This is a heading 1."
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.HEADING
        )

    def test_block_to_block_type_h6(self):
        block = "###### This is a heading 6."
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.HEADING
        )

    def test_block_to_block_type_invalid_heading(self):
        block = "####### This is a naughty heading 7."
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block```"
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        block = "> This is a multiline quote block\n> This is the second line"
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.QUOTE
        )

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a multiline unordered list block\n- This is the second line"
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is a multiline ordered list block\n2. This is the second line"
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_ordered_list_bad_start(self):
        block = "2. This is a multiline ordered list block\n3. But it starts at 2!"
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ordered_list_number_skip(self):
        block = "1. This is a multiline ordered list block\n3. But it skips 2!"
        blocktype = block_to_block_type(block)
        self.assertEqual(
            blocktype,
            BlockType.PARAGRAPH
        )

    # test block to HTML
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
    )
        
    def test_unordered_list(self):
        md = """
- This is **bolded** paragraph
- This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bolded</b> paragraph</li><li>This is another paragraph with <i>italic</i> text and <code>code</code> here</li></ul></div>",
        )
        
    def test_ordered_list(self):
        md = """
1. This is **bolded** paragraph
2. This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bolded</b> paragraph</li><li>This is another paragraph with <i>italic</i> text and <code>code</code> here</li></ol></div>",
        )

    def test_h1_blockquote(self):
        md = """
# Here are some cool quotes:

> This quote is 
> so neat, right?

> This one too, right?
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Here are some cool quotes:</h1><blockquote>This quote is \nso neat, right?</blockquote><blockquote>This one too, right?</blockquote></div>",
        )

    def test_empty_string_to_html(self):
        md = ""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div></div>",
        )

    def test_extract_title(self):
        self.assertEqual(
            extract_title("# Test heading"),
            "Test heading"
        )

    def test_extract_title_exception(self):
        with self.assertRaises(Exception):
            extract_title("Test heading")