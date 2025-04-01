import os
import sys
sys.path.append(os.path.abspath("./src"))

from markdown_scanner.block_scanner import markdown_to_blocks
import unittest


class TestBlockMarkdown(unittest.TestCase):
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

    def test_with_empty_blocks(self):
        md = """




This is **bolded paragraph**

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
- and more items




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded paragraph**",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items\n- and more items",
            ],
        )

    def test_with_only_white_blocks(self):
        md = """





"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])

if __name__ == "__main__":
    unittest.main()