from node.leafnode import LeafNode
from node.parentnode import ParentNode

node = LeafNode("p", "Some content")
parent = ParentNode("div", [node])
parent.to_html()
