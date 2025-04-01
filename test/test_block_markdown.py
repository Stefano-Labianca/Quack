import os
import sys
sys.path.append(os.path.abspath("./src"))

from markdown_scanner.block_scanner import BlockType, block_to_block_type, markdown_to_blocks
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


    def test_markdown_block_type(self):
        md = """
This should
all be
one match

# this should match heading

### this should also match heading

1. one 
2. two 
3. three 

- one
- two
- three

> Star quote block
> Another quote

this should be a second match
Another paragrah

and again

```
const foo = "bar"
```
"""
        blocks = markdown_to_blocks(md)
        b_types = []
        for block in blocks:
            t = block_to_block_type(block)
            b_types.append(t)

        self.assertListEqual(
            [
                BlockType.PARAGRAPH, BlockType.HEADING, BlockType.HEADING, 
                BlockType.ORDERED_LIST,BlockType.UNORDERED_LIST, BlockType.QUOTE,
                BlockType.PARAGRAPH, BlockType.PARAGRAPH, BlockType.CODE
            ],
            b_types
        )

if __name__ == "__main__":
    unittest.main()