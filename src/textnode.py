from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plaintext"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        same_text = self.text == other.text
        same_text_type = self.text_type == other.text_type
        same_url = self.url == other.url
        return same_text and same_text_type and same_url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"