class AllNoneArgumentsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict[str, any] | None = None):
        """
        ### HTMLNode
        - `tag`: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        - `value`: A string representing the value of the HTML tag 
        - `children`: A list of `HTMLNode` objects representing the children of this node
        - `props`: A dictionary of key-value pairs representing the attributes of the HTML tag. 
        For example, a link (`<a>` tag) might have `{"href": "https://www.google.com"}`

        ### Implementation Notes
        - An `HTMLNode` without a `tag` will just render as raw text
        - An `HTMLNode` without a `value` will be assumed to have children
        - An `HTMLNode` without `children` will be assumed to have a value
        - An `HTMLNode` without `props` simply won't have any attributes
        """

        if tag == None and value == None and children == None and props == None:
            raise AllNoneArgumentsError(
                "Cannot pass all None arguments to HTMLNode"
            )

        if value == None and children == None:
            raise ValueError(
                "Argument `value` and `children` cannot be both empty or None"
            )

        if value != None and children != None and len(children) > 0:
            raise ValueError(
                "HTMLNode cannot have both `value` and `children` set. Pick one."
            )

        if tag != None and not isinstance(tag, str):
            raise TypeError("`tag` must be a string")

        if value != None and not isinstance(value, str):
            raise TypeError("`value` must be a string")

        if children != None and not isinstance(children, list):
            raise TypeError("`children` must be a list")

        if props != None and not isinstance(props, dict):
            raise TypeError("`props` must be a dictionary")

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""

        str_props = " "
        items = self.props.items()

        for k, v in items:
            str_props += f"{k}=\"{v}\" "

        return str_props.rstrip(" ")

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
