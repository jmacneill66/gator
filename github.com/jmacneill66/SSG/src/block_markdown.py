import re
from htmlnode import LeafNode
from enum import Enum


def markdown_to_blocks(markdown):
    string_blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in string_blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks
