import unittest

from src.nodes.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Me!",  {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), "<a href=\"https://www.google.com\">Click Me!</a>"
        )

    def test_leaf_to_html_row_text(self):
        node = LeafNode(None, value="I am a simple text!")
        self.assertEqual(
            node.to_html(), "I am a simple text!"
        )

    def test_missing_tag_from_leaf_with_props(self):
        node = LeafNode(None, "Dummy node", {"href": "https://www.google.com"})
        self.assertRaises(
            ValueError,
            lambda *args, **kwargs: node.to_html()
        )

    def test_escape_chars(self):
        node = LeafNode("p", "<Hello '& \"World\">")
        self.assertEqual(
            node.to_html(), "<p>&lt;Hello &#x27;&amp; &quot;World&quot;&gt;</p>"
        )


if __name__ == "__main__":
    unittest.main()
