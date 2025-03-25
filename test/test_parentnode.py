import unittest

from src.node.leafnode import LeafNode
from src.node.parentnode import InvalidHTMLNodeError, ParentNode


class TestParentNode(unittest.TestCase):
    def test_simple_parent(self):
        full_str = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        created_str = node.to_html()
        self.assertEqual(full_str, created_str)

    def test_multiple_parents(self):
        full_str = "<p><div><b>Bold text</b>Normal text</div><div><i>italic text</i>Normal text</div></p>"
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "div",
                    [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]
                ),
                ParentNode(
                    "div",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text")
                    ]
                ),
            ],
        )

        created_str = node.to_html()
        self.assertEqual(full_str, created_str)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_and_childre_with_props(self):
        childrens = [
            LeafNode("b", "Bold text"),
            LeafNode("a", "A Link text", {"href": "https://www.google.com"})
        ]

        parent = ParentNode("div", childrens, {"class": "w-full"})
        self.assertEqual(
            parent.to_html(),
            "<div class=\"w-full\"><b>Bold text</b><a href=\"https://www.google.com\">A Link text</a></div>",
        )

    def test_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(
            parent.to_html(),
            "<div></div>",
        )

    def test_empty_children_and_props(self):
        parent = ParentNode("div", [], {"class": "w-full"})
        self.assertEqual(
            parent.to_html(),
            "<div class=\"w-full\"></div>",
        )

    def test_none_parent_tag(self):
        parent = ParentNode(None, [])
        self.assertRaises(
            ValueError,
            lambda *args, **kwargs: parent.to_html()
        )

    def test_parent_with_empty_values(self):
        childrens = [
            LeafNode("b", " "),
            LeafNode("a", "")
        ]

        parent = ParentNode("div", childrens, {"class": "w-full"})
        self.assertEqual(
            parent.to_html(),
            "<div class=\"w-full\"><b> </b><a></a></div>"
        )

    def test_invalid_children(self):
        self.assertRaises(
            ValueError,
            lambda *args, **kwargs: ParentNode("p", None)
        )

    def test_invalid_child_with_none_as_value(self):
        childrens = [
            LeafNode("a", None, {"href": "https://www.google.com"})
        ]

        parent = ParentNode("div", childrens, {"class": "w-full"})
        self.assertRaises(
            ValueError,
            lambda *args, **kwargs: parent.to_html()
        )

    def test_invalid_child_with_none_as_tag_and_props(self):
        childrens = [
            LeafNode(None, "A link", {"href": "https://www.google.com"})
        ]

        parent = ParentNode("div", childrens, {"class": "w-full"})
        self.assertRaises(
            ValueError,
            lambda *args, **kwargs: parent.to_html()
        )

    def test_non_valid_children_type(self):
        node = LeafNode("p", "Some content")
        parent = ParentNode("div", [node, "bvbb"])

        self.assertRaises(
            InvalidHTMLNodeError,
            lambda *args, **kwargs: parent.to_html()
        )


if __name__ == "__main__":
    unittest.main()
