import unittest

from src.converter.converter import text_node_to_html_node
from src.node.textnode import InvalidTextNodeError, TextNode, TextType


class TestTextNodeToHTMLNodeConverter(unittest.TestCase):
    def test_text_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_node(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic_node(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code_node(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link_node(self):
        node = TextNode(
            "This is a link node",
            TextType.LINK,
            "https://www.google.com"
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(
            html_node.props_to_html(),
            " href=\"https://www.google.com\""
        )

    def test_image_node(self):
        node = TextNode(
            "This is my alt text",
            TextType.IMAGE,
            "http://localhost:8080/img/1"
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props_to_html(),
            f" src=\"{node.url}\" alt=\"{node.text}\""
        )


if __name__ == "__main__":
    unittest.main()
