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