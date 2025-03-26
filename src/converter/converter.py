from src.node.leafnode import LeafNode
from src.node.textnode import InvalidTextNodeError, TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url == None:
                raise InvalidTextNodeError(
                    "TextType.LINK cannot have None url"
                )

            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url == None:
                raise InvalidTextNodeError(
                    "TextType.IMAGE cannot have None url"
                )

            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
