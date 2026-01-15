# src/test_htmlnode.py HTMLNode class tests

import unittest
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_empty_node_creation(self):
        node = HTMLNode()
        print(node)
        self.assertIsInstance(node, HTMLNode)
    
    def test_eq_headers(self):
        print("eq_headers")
        node = HTMLNode(tag="h1", value="Hello world")
        print(f"Node 1:\n{node}")

        node2 = HTMLNode(tag="h1", value="Hello world")
        print(f"Node 2:\n{node2}")

        self.assertEqual(repr(node), repr(node2))

    def test_parent_child(self):
        node = HTMLNode(
            tag="a",
            value="Boot.dev link",
            props={"href": "https://www.boot.dev"}
            )
        print(f"Child:\n{node}")

        parent_node = HTMLNode(
            tag="p",
            children=node
            )
        print(f"Parent:\n{parent_node}")
        
        self.assertIsInstance(node, HTMLNode)
        self.assertIsInstance(parent_node, HTMLNode)

    def test_not_eq_anchors(self):
        node = HTMLNode(
            tag="a",
            value="Boot.dev link",
            props={"href": "https://www.boot.dev"}
            )
        print(f"Correct link:\n{node}")

        node2 = HTMLNode(
            tag="a",
            value="Boot.dev link",
            props={"href": "https://www.google.com"}
            )
        print(f"Incorrect link:\n{node2}")

        self.assertNotEqual(repr(node), repr(node2))