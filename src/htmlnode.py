#!/usr/bin/env python

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = ""
        for prop in self.props:
            props_string += f' "{prop}"={self.props[prop]}'
        return props_string

    def __repr__(self):
        return f"""
        tag={self.tag}
        value={self.value}
        children={self.children}
        props={self.props_to_html()}
        """
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"""
        tag={self.tag}
        value={self.value}
        props={self.props_to_html()}
        """
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have children")
        
        html_string = f"<{self.tag}>"

        for child in self.children:
            html_string += child.to_html()

        html_string += f"</{self.tag}>"

        return html_string