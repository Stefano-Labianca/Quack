import html

from .htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        """
        ### LeafNode
        A `LeafNode` rappresent an HTML tag without children

        - `tag`: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        - `value`: A string representing the value of the HTML tag 
        - `props`: A dictionary of key-value pairs representing the attributes of the HTML tag. 
        For example, a link (`<a>` tag) might have `{"href": "https://www.google.com"}`
        """
        if value != None:
            value = html.escape(value, False)

        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag == None and self.props != None:
            raise ValueError("`props` cannot be assigned to None tag")

        if self.tag == None:
            return self.value

        str_props = self.props_to_html()
        return f"<{self.tag}{str_props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
