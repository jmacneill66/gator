import unittest


from textnode import *


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
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
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

    def test_extract_markdown_images(self):
        match = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], match)

    def test_extract_markdown_links(self):
        match = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            match,
        )


def test_extract_markdown_images():
    assert extract_markdown_images("![alt text](https://example.com/image.png)") == [
        ("alt text", "https://example.com/image.png")]
    assert extract_markdown_images("No images here!") == []


def test_extract_markdown_links():
    assert extract_markdown_links(
        "[click here](https://example.com)") == [("click here", "https://example.com")]
    assert extract_markdown_links("No links here!") == []


def test_split_nodes_image():
    node = TextNode(
        "Here is an ![image](https://example.com/image.png) in text", TextType.TEXT)
    new_nodes = split_nodes_image([node])
    assert new_nodes == [
        TextNode("Here is an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        TextNode(" in text", TextType.TEXT)
    ]


def test_split_nodes_link():
    node = TextNode(
        "Click [here](https://example.com) to continue", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    assert new_nodes == [
        TextNode("Click ", TextType.TEXT),
        TextNode("here", TextType.LINK, "https://example.com"),
        TextNode(" to continue", TextType.TEXT)
    ]


def test_text_to_textnodes(self):
    text = "This is **bold** and *italic* and `code` and a [link](https://example.com) and ![image](https://example.com/image.png)"
    nodes = text_to_textnodes(text)
    assert nodes == [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" and ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://example.com"),
        TextNode(" and ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://example.com/image.png")
    ]


if __name__ == "__main__":
    unittest.main()
