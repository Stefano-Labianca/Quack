from markdown_scanner.inline_scanner import split_nodes_delimiter, split_nodes_image, split_nodes_link
from nodes.leafnode import LeafNode
from nodes.textnode import InvalidTextNodeError, TextNode, TextType


class SplitPipeline:
    def __init__(self, md_str: str) -> None:
        self.__nodes: list[TextNode] = [TextNode(md_str, TextType.TEXT)]

    def bold(self):
        self.__nodes = split_nodes_delimiter(self.__nodes, "**", TextType.BOLD)
        return self
    
    def italic(self):
        self.__nodes = split_nodes_delimiter(self.__nodes, "_", TextType.ITALIC)
        return self
    
    def code(self):
        self.__nodes = split_nodes_delimiter(self.__nodes, "`", TextType.CODE)
        return self
    
    def image(self):
        self.__nodes = split_nodes_image(self.__nodes)
        return self

    def link(self):
        self.__nodes = split_nodes_link(self.__nodes)
        return self
    
    def end(self):
        return self.__nodes

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

def text_to_textnodes(text: str):
    pipeline = SplitPipeline(text)
    pipeline = pipeline.bold().italic().code().image().link()
  
    return pipeline.end()

