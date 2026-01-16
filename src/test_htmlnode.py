#!/usr/bin/env python

import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_node_creation(self):
        node = HTMLNode()
        # print(node)
        self.assertIsInstance(node, HTMLNode)
    
    def test_eq_headers(self):
        # print("eq_headers")
        node = LeafNode(tag="h1", value="Hello world")
        # print(f"Node 1:\n{node}")

        node2 = LeafNode(tag="h1", value="Hello world")
        # print(f"Node 2:\n{node2}")

        self.assertEqual(repr(node), repr(node2))

    def test_parent_child(self):
        node = LeafNode(
            tag="a",
            value="Boot.dev link",
            props={"href": "https://www.boot.dev"}
            )
        # print(f"Child:\n{node}")

        parent_node = HTMLNode(
            tag="p",
            children=node
            )
        # print(f"Parent:\n{parent_node}")
        
        self.assertIsInstance(node, LeafNode)
        self.assertIsInstance(parent_node, HTMLNode)

    def test_not_eq_anchors(self):
        node = HTMLNode(
            tag="a",
            value="Boot.dev link",
            props={"href": "https://www.boot.dev"}
            )
        # print(f"Correct link:\n{node}")

        node2 = HTMLNode(
            tag="a",
            value="Boot.dev link",
            props={"href": "https://www.google.com"}
            )
        # print(f"Incorrect link:\n{node2}")

        self.assertNotEqual(repr(node), repr(node2))

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("b", "child1")
        child_node2 = LeafNode("i", "child2")
        parent_node = ParentNode("p", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>child1</b><i>child2</i></p>"
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("p", None)
        self.assertRaises(
            ValueError, parent_node.to_html
        )