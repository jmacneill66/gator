# Unit tests
import unittest
from block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type(
            "###### Smallest heading"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(block_to_block_type(
            "```code here```"), BlockType.CODE)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type(
            "> This is a quote\n> Another line"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type(
            "- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type(
            "1. First\n2. Second"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type(
            "Just a simple paragraph."), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
