from node.leafnode import LeafNode
from node.parentnode import ParentNode

node = LeafNode("p", "Some content")
parent = ParentNode("div", [node, "bvbb"])
parent.to_html()
