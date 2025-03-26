from scanner import split_nodes_delimiter
from nodes.textnode import TextNode, TextType

code = TextNode("This is text with a `code block` word", TextType.TEXT)

new_nodes = split_nodes_delimiter([code], "`", TextType.CODE)
print(new_nodes)

italics = [
    TextNode("This is text with a _italic block_ word", TextType.TEXT),
    TextNode("This is _text with a _italic block_ word", TextType.TEXT),
    TextNode("_Just one italic block_", TextType.TEXT),
    TextNode("_Just one italic_ block_", TextType.TEXT),
]


new_nodes = split_nodes_delimiter(italics, "_", TextType.ITALIC)
print(new_nodes)