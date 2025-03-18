from textnode import TextNode, TextType

node = TextNode("This is some anchor text",
                TextType.LINK, "https://www.boot.dev")

another_node = TextNode("This is some  text",
                        TextType.LINK, "https://www.boot.dev")

print(node)
