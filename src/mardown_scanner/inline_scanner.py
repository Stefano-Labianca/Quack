from typing import Literal
from nodes.textnode import TextNode, TextType
import re 

MARKDOWN_IMAGE_REGEX = r"!\[(.*?)\]\(([^\(\)]*)\)"
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
        images = re.findall(MARKDOWN_IMAGE_REGEX, text)

        for image in images:
            brachets_stack: list[str] = []
            alt_content: str = image[0]

            if ("[" not in alt_content) and ("]" not in alt_content):
                continue

            for symbol in alt_content:
                if symbol == "]" and len(brachets_stack) == 0:
                    raise MalformattedMarkdownError(f"Malformatted image: {image}")

                if symbol == "[":
                    brachets_stack.append(symbol)
                elif symbol == "]":
                    brachets_stack.pop()

            if len(brachets_stack) > 0:
                raise MalformattedMarkdownError(f"Malformatted image: {image}")

        return images
        


    def extract_markdown_links(text: str):
        simple_links = re.findall(MARKDOWN_LINK_REGEX, text)

        # TODO: Handle Nested alt for links and image links inside a link
        # TODO: Need more test for this regex on links: (?<!!)\[([^\[\]].*?)\]\(([^\(\)]*)\)
        return simple_links

    if link_type == "image":
        return extract_markdown_images
    if link_type == "link":
        return extract_markdown_links