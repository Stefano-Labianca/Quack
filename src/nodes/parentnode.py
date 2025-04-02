from .htmlnode import HTMLNode


class InvalidHTMLNodeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ParentNode(HTMLNode):
    """
    ### ParentNode
    A `ParentNode` rappresent an HTML tag with children

    - `tag`: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    - `children`: A list of `HTMLNode` objects representing the children of this node
    - `props`: A dictionary of key-value pairs representing the attributes of the HTML tag. 
        For example, a link (`<a>` tag) might have `{"href": "https://www.google.com"}`
    """

    def __init__(self, tag: str, children: list, props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must have a valid tag")

        if self.children == None:
            raise ValueError("Parent node can not have None as `children`")

        nodes = ""
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise InvalidHTMLNodeError(
                    f"The following child is not a class or a subclass of HTMLNode: {child}"
                )

            nodes += child.to_html()

        str_props = self.props_to_html()
        return f"<{self.tag}{str_props}>{nodes}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
