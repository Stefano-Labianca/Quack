from enum import Enum


class TextType(Enum):
    NORMAL = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        """
        ### TextNode
            - `text`: Text content of the node
            - `text_type`: The type of text this node contains, which is a  member of the `TextType` enum
            - `url`: The URL of the link or image, if the text is a link. Default to None if nothing is passed in.
        """

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"
