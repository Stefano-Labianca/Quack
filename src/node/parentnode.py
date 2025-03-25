from .htmlnode import HTMLNode


class InvalidHTMLNodeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, any] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must have a valid tag")

        nodes = ""
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise InvalidHTMLNodeError(
                    f"The following child is not a class or a subclass of HTMLNode: {child}"
                )

            nodes += child.to_html()

        str_props = self.props_to_html()
        return f"<{self.tag}{str_props}>{nodes}</{self.tag}>"
