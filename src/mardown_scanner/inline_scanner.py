from typing import Literal
from nodes.textnode import TextNode, TextType
import re 

MARKDOWN_IMAGE_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
MARKDOWN_LINK_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

class MalformattedMarkdownError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise MalformattedMarkdownError(f"Malformatted block for delimiter '{delimiter}' -> {old_node.text}")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
        
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_links(link_type: Literal["image"] | Literal["link"]):
    def extract_markdown_images(text: str):        
        return re.findall(MARKDOWN_IMAGE_REGEX, text)

    def extract_markdown_links(text: str):
        return re.findall(MARKDOWN_LINK_REGEX, text)
    
    if link_type == "image":
        return extract_markdown_images
    if link_type == "link":
        return extract_markdown_links