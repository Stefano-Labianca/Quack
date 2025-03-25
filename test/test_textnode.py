import unittest

from src.node.textnode import TextNode, TextType


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

    def test_invalid_text_type(self):
        self.assertRaises(AttributeError,
                          lambda *args, **kwargs: TextNode(
                              "This is a text node", TextType.INVALID)
                          )

    def test_link_is_not_none(self):
        node = TextNode("This is a text node", TextType.BOLD,
                        "https://docs.python.org/3/library/unittest.html")

        self.assertIsNotNone(node.url)


if __name__ == "__main__":
    unittest.main()
