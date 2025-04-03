from markdown_scanner.block_scanner import BlockType, block_to_block_type, markdown_to_blocks
from markdown_scanner.inline_scanner import MalformattedMarkdownError, split_nodes_delimiter, split_nodes_image, split_nodes_link
from nodes.htmlnode import HTMLNode
from nodes.leafnode import LeafNode
from nodes.parentnode import ParentNode
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


def block_node_to_html_node(block: str) -> tuple[BlockType, HTMLNode]:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return (BlockType.PARAGRAPH, ParentNode("p", []))
        
        case BlockType.QUOTE:
            return (BlockType.QUOTE, ParentNode("blockquote", []))
        
        case BlockType.UNORDERED_LIST:
            return (BlockType.UNORDERED_LIST, ParentNode("ul", []))
        
        case BlockType.ORDERED_LIST:
            return (BlockType.ORDERED_LIST, ParentNode("ol", []))
        
        case BlockType.CODE:
            return (BlockType.CODE, ParentNode("pre", []))
        
        case BlockType.HEADING:
            hash_amount = count_heading_hash(block)

            if hash_amount + 1 >= len(block):
                raise MalformattedMarkdownError(f"invalid heading level: {hash_amount}")

            heading_tag = f"h{hash_amount}"

            return (BlockType.HEADING, ParentNode(heading_tag, []))


def text_to_textnodes(text: str) -> list[TextNode]:
    pipeline = SplitPipeline(text)
    pipeline = pipeline.bold().italic().code().image().link()
    
    return pipeline.end()


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    title = blocks[0]
    
    if not title.startswith("# "):
        raise Exception("No title found")
    
    return title.lstrip("# ").strip()
        


def markdown_to_html_node(document: str) -> ParentNode:
    blocks = markdown_to_blocks(document)
    parents: list[HTMLNode] = []
    root = ParentNode("div", children=[])

    for block in blocks:
        parent_type, parent = block_node_to_html_node(block)
        children_generator = text_to_children_fn(parent_type)
        parent.children = children_generator(block)
        parents.append(parent)

    root.children = parents

    return root


def text_to_children_fn(block_type: BlockType):
    match block_type:
        case BlockType.PARAGRAPH:
            return text_to_children_paragraph
        
        case BlockType.HEADING:
            return text_to_children_heading
        
        case BlockType.QUOTE:
            return text_to_children_quote
        
        case BlockType.UNORDERED_LIST:
            return text_to_children_unordered_list
        
        case BlockType.ORDERED_LIST:
            return text_to_children_ordered_list
        
        case BlockType.CODE:
            return text_to_children_code_block
        

def text_to_children_code_block(text: str) -> list[LeafNode]:
    if not text.startswith("```") or not text.endswith("```"):
        raise MalformattedMarkdownError("invalid code block")

    text = text.replace("```", "").replace("\n", "", 1)
    code_node = TextNode(text, TextType.CODE)
    code_tag = text_node_to_html_node(code_node)

    return [code_tag]


def text_to_children_ordered_list(text: str) -> list[ParentNode]:
    lines = text.split("\n")
    element = []

    for line in lines:
        line = line[3:].strip()
        children = text_to_children_paragraph(line)
        li = ParentNode("li", children)
        element.append(li)

    return element


def text_to_children_unordered_list(text: str) -> list[ParentNode]:
    text = text.replace("- ", "")
    lines = text.split("\n")
    element = []

    for line in lines:
        children = text_to_children_paragraph(line)
        li = ParentNode("li", children)
        element.append(li)

    return element


def text_to_children_quote(text: str) -> list[LeafNode]:
    lines = text.split("\n")

    for line in lines:
        if not line.startswith(">"):
            raise MalformattedMarkdownError("invalid quote block")

    text = text.replace(">", "")
    new_lines = []

    for line in lines:
        new_lines.append(line[2:].strip())

    content = " ".join(new_lines)
    node = LeafNode(None, content)

    return [node]



def text_to_children_heading(text: str):
    hash_amount = count_heading_hash(text)

    if hash_amount + 1 >= len(text):
        raise MalformattedMarkdownError(f"invalid heading level: {hash_amount}")

    heading_content = text.split(f"{'#' * hash_amount} ")[1]

    children: list[LeafNode] = []
    nodes = text_to_textnodes(heading_content)

    for node in nodes:
        child = text_node_to_html_node(node)
        children.append(child)

    return children


def text_to_children_paragraph(text: str) -> list[LeafNode]:
    children: list[LeafNode] = []
    lines = text.split("\n")

    for idx in range(len(lines)):
        line = lines[idx]
        
        if idx != len(lines) - 1:
            line = f"{line} "

        nodes = text_to_textnodes(line)

        for node in nodes:
            child = text_node_to_html_node(node)
            children.append(child)

    return children


def count_heading_hash(heading: str) -> int:
    amount = 0

    for c in heading:
        if c == "#":
            amount += 1
        else:
            break

    return amount
