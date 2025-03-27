import unittest

from mardown_scanner.inline_scanner import MalformattedMarkdownError, split_nodes_delimiter, extract_links
from nodes.textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extractor = extract_links("image")
        content = extractor(text)

        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ], 
            content
        )

    def test_no_images(self):
        text = "Here is some text with no images at all."
        extractor = extract_links("image")
        content = extractor(text)

        self.assertListEqual([], content)

    def test_nested_alt(self):
        text = "![image [with nested] alt text](https://example.com/image.png)"
        extractor = extract_links("image")
        content = extractor(text)

        self.assertListEqual([('image [with nested] alt text', 'https://example.com/image.png')], content)

    def test_deep_nested_alt(self):
        text = "![alt [nested [more nested]]](https://example.com/img.jpeg)"
        extractor = extract_links("image")
        content = extractor(text)

        self.assertListEqual([('alt [nested [more nested]]', 'https://example.com/img.jpeg')], content)

    def test_nested_and_simple_image_alt(self):
        text = "This is text with a ![rick [roll]](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extractor = extract_links("image")
        content = extractor(text)

        self.assertListEqual(
            [('rick [roll]', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')],
            content
        )
    
    def test_multiple_nested_alt(self):
        text = "![alt nested [more nested]](https://example.com/img.jpeg) and ![again alt nested [more nested]](https://example.com/img.jpeg)"
        extractor = extract_links("image")
        content = extractor(text)

        self.assertListEqual(
            [('alt nested [more nested]', 'https://example.com/img.jpeg'), ('again alt nested [more nested]', 'https://example.com/img.jpeg')],
            content
        )

    def test_invalid_alt(self):
        extractor = extract_links("image")
        text = "![invalid [alt]]](https://example.com/img.jpeg)"
        self.assertRaises(MalformattedMarkdownError, lambda *args, **kwargs: extractor(text)) 

    def test_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extractor = extract_links("link")
        content = extractor(text)

        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
            ], 
            content
        )

    def test_no_links(self):
        text = "Here is some text with no links at all."
        extractor = extract_links("link")
        content = extractor(text)
        
        self.assertListEqual([], content)