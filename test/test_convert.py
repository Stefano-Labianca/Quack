import unittest
import os
import sys
sys.path.append(os.path.abspath("./src"))

from nodes.textnode import TextNode, TextType
from convert import text_node_to_html_node, text_to_textnodes




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

    def test_text_to_textnodes_full(self):
        full_md_str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(full_md_str)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_without_links_and_images(self):
        md_str = "This is **text** with an _italic_ word and a `code block` and an"
        nodes = text_to_textnodes(md_str)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an", TextType.TEXT)
        ]

        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_str(self):
        md_str = "This is text with an italic word and a code block and an"
        nodes = text_to_textnodes(md_str)
        expected = [
            TextNode("This is text with an italic word and a code block and an", TextType.TEXT),
        ]

        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_with_only_italic(self):
        md_str = "This is text with an _italic_ word and a code block and an"
        nodes = text_to_textnodes(md_str)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a code block and an", TextType.TEXT),
        ]

        self.assertListEqual(expected, nodes)

if __name__ == "__main__":
    unittest.main()
