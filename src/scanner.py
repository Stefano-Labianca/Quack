from nodes.textnode import TextNode, TextType

class MalformattedMarkdownError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # TODO: Upgrade it to better handle opening and closing delimiter
        text = node.text
        if text.count(delimiter) % 2 == 1:
            raise MalformattedMarkdownError(f"Markdown string malformatted for node: {node}")
        
        

    return new_nodes                

