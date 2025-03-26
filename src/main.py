from scanner import split_nodes_delimiter
from nodes.textnode import TextNode, TextType

code = TextNode("`This` is text with a `code block` word. `Funny guy`", TextType.TEXT)
code2 = TextNode("This is `text` with a `code block` word. `Funny guy`", TextType.TEXT)
code3 = TextNode("`This is` text with a `code block` word. Funny guy.", TextType.TEXT)
new_nodes = split_nodes_delimiter([code, code2, code3], "`", TextType.CODE)
print(new_nodes)

italics = [
    TextNode("This is text with a _italic block_ word", TextType.TEXT),
    TextNode("_Just one italic block_", TextType.TEXT),
]


new_nodes = split_nodes_delimiter(italics, "_", TextType.ITALIC)
print("\n-------\n")

