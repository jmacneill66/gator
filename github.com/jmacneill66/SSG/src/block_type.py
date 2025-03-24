from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # Check for heading
    if re.match(r"^#{1,6} \S", block):
        return BlockType.HEADING

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Check for quote block
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list
    if all(re.match(r"^- \S", line) for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list
    if all(re.match(rf"^{i+1}\. \S", line) for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # Default to paragraph
    return BlockType.PARAGRAPH
