import re
from htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_to_html(textnode):
    if textnode.text_type == TextType.TEXT:
        return LeafNode(None, textnode.text)
    if textnode.text_type == TextType.BOLD:
        return LeafNode("b", textnode.text)
    if textnode.text_type == TextType.ITALIC:
        return LeafNode("i", textnode.text)
    if textnode.text_type == TextType.CODE:
        return LeafNode("code", textnode.text)
    if textnode.text_type == TextType.LINK:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    if textnode.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
    raise ValueError(f"invalid text type: {textnode.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: unclosed delimiter '{delimiter}' in {node.text}")
        for i, part in enumerate(parts):
            if part:
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = re.split(r'(!\[.*?\]\(.*?\))', node.text)
        for part in parts:
            match = re.match(r'!\[(.*?)\]\((.*?)\)', part)
            if match:
                new_nodes.append(TextNode(match.group(
                    1), TextType.IMAGE, match.group(2)))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = re.split(r'(\[.*?\]\(.*?\))', node.text)
        for part in parts:
            match = re.match(r'\[(.*?)\]\((.*?)\)', part)
            if match:
                new_nodes.append(TextNode(match.group(
                    1), TextType.LINK, match.group(2)))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
