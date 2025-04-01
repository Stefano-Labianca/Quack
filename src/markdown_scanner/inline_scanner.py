from typing import Any, Literal
from nodes.textnode import TextNode, TextType
import re 

MARKDOWN_IMAGE_REGEX = r"!\[(.*?)\]\(([^\(\)]*)\)"
MARKDOWN_LINK_REGEX = r"(?<!!)\[([^\[\]].*?)\]\(([^\(\)]*)\)"

class MalformattedMarkdownError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        split_nodes: list[TextNode] = []
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


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []
    image_extractor = extract_links("image")

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        content = old_node.text
        parsed_images = image_extractor(old_node.text)
        
        if len(parsed_images) == 0:
            new_nodes.append(old_node)
            continue

        for parsed_image in parsed_images:
            image_alt = parsed_image[0]
            image_link = parsed_image[1]

            sections = content.split(f"![{image_alt}]({image_link})", 1)
            text_part = sections[0]
            content = sections[1]

            new_nodes.append(
                TextNode(text_part, TextType.TEXT)
            )

            new_nodes.append(
                TextNode(image_alt, TextType.IMAGE, image_link)
            )
        
        if content != "":
            new_nodes.append(
                TextNode(content, TextType.TEXT)
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []
    link_extractor = extract_links("link")

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        content = old_node.text
        parsed_links = link_extractor(old_node.text)

        if len(parsed_links) == 0:
            new_nodes.append(old_node)
            continue

        for parsed_link in parsed_links:
            link_alt = parsed_link[0]
            link_url = parsed_link[1]

            sections = content.split(f"[{link_alt}]({link_url})", 1)
            text_part = sections[0]
            content = sections[1]

            new_nodes.append(
                TextNode(text_part, TextType.TEXT)
            )

            new_nodes.append(
                TextNode(link_alt, TextType.LINK, link_url)
            )
          
        if content != "":
            new_nodes.append(
                TextNode(content, TextType.TEXT)
            )


    return new_nodes


def extract_links(link_type: Literal["image"] | Literal["link"]):
    def extract_markdown_images(text: str):        
        images = re.findall(MARKDOWN_IMAGE_REGEX, text)
        err = __validate_alt_content(images)
        
        if err != None:
            raise err

        return images
        

    def extract_markdown_links(text: str):
        links = re.findall(MARKDOWN_LINK_REGEX, text)
        err = __validate_alt_content(links)

        if err != None:
            raise err

        return links

    if link_type == "image":
        return extract_markdown_images
    if link_type == "link":
        return extract_markdown_links
    

def __validate_alt_content(links: list[Any]):
    for link in links:
        brachets_stack: list[str] = []
        alt_content: str = link[0]

        if ("[" not in alt_content) and ("]" not in alt_content):
            continue

        for symbol in alt_content:
            if symbol == "]" and len(brachets_stack) == 0:
                return MalformattedMarkdownError(f"Malformatted link or image: {link}")

            if symbol == "[":
                brachets_stack.append(symbol)
            elif symbol == "]":
                brachets_stack.pop()

        if len(brachets_stack) > 0:
            return MalformattedMarkdownError(f"Malformatted link or image: {link}")
    return None