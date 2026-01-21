#!/usr/bin/env python

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "hearing"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"