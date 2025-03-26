from convert import text_node_to_html_node
from nodes.textnode import TextNode, TextType

node = TextNode("I am a link", TextType.LINK, "https://www.google.com")
print(text_node_to_html_node(node))
