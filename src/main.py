from mardown_scanner.inline_scanner import split_nodes_delimiter
from nodes.textnode import TextNode, TextType

# codes = [
#     TextNode("`This` is text with a `code block` word. `Funny guy`", TextType.TEXT),
#     TextNode("This is `text` with a `code block` word. `Funny guy`", TextType.TEXT),
#     TextNode("`This is` text with a `code block` word. Funny guy.", TextType.TEXT)
# ]


# new_nodes = split_nodes_delimiter(codes, "`", TextType.CODE)
# print(new_nodes)
# print("\n-------\n")

italics = [
    TextNode("_This is text_ with a _italic block_ word", TextType.TEXT),
    TextNode("_Just one italic block_", TextType.TEXT),
]

# new_nodes = split_nodes_delimiter(italics, "_", TextType.ITALIC)
# print("\n-------\n")

# bolds = [
#     TextNode("This is text with a **bold  block** word", TextType.TEXT),
#     TextNode("**Just one bold block**", TextType.TEXT),
#     TextNode("**Just one bold block**. Salame e pepe e **fagioli** con *gelato", TextType.TEXT),
# ]

print("Solution")
new_nodes = split_nodes_delimiter(italics, "_", TextType.ITALIC)
print(new_nodes)
