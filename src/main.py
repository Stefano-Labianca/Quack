from convert import text_to_textnodes
from mardown_scanner.inline_scanner import split_nodes_image
from nodes.textnode import TextNode, TextType


full_md_str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
nodes = text_to_textnodes(full_md_str)

print(nodes)
