import unittest

from src.nodes.htmlnode import AllNoneArgumentsError, HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_is_none(self):
        node = HTMLNode("a", "A dummy link")
        props = node.props_to_html()

        self.assertEqual(props, "")

    def test_props_to_html_is_empty_dict(self):
        node = HTMLNode("a", "A dummy link", props={})
        props = node.props_to_html()

        self.assertEqual(props, "")

    def test_generated_props(self):
        test_str = " href=\"https://www.google.com\" target=\"_blank\""
        props = {"href": "https://www.google.com", "target": "_blank"}

        node = HTMLNode("a", "Link to Google", props=props)
        generated_props = node.props_to_html()

        self.assertEqual(test_str, generated_props)

    def test_all_none_arguments(self):
        self.assertRaises(
            AllNoneArgumentsError,
            lambda *args, **kwargs: HTMLNode()
        )

    def test_value_and_children_are_none(self):
        self.assertRaises(
            ValueError,
            lambda *args, **kwargs: HTMLNode("p")
        )

    def test_value_and_children_are_both_passed(self):
        nodes = [
            HTMLNode("p", "One"),
            HTMLNode("p", "Two"),
            HTMLNode("p", "Three"),
        ]

        self.assertRaises(
            ValueError,
            lambda *args, **kwargs: HTMLNode("div", "Some content", nodes)
        )


if __name__ == "__main__":
    unittest.main()
