import unittest

from src.nodes.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node",
                         TextType.ITALIC, "http://localhost")
        self.assertNotEqual(node, node2)

    def test_link_is_not_none(self):
        node = TextNode("This is a text node", TextType.BOLD,
                        "https://docs.python.org/3/library/unittest.html")

        self.assertIsNotNone(node.url)


if __name__ == "__main__":
    unittest.main()
