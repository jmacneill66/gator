from operator import index
from tempfile import template
from textnode import *
from md_to_html_node import *
from htmlnode import *
import shutil
import os


def copy_directory(src: str, dest: str):
    """Recursively copies all contents from src to dest, ensuring a clean copy."""
    if os.path.exists(dest):
        shutil.rmtree(dest)  # Remove existing destination directory

    os.makedirs(dest)  # Create a fresh destination directory

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            # Recursively copy subdirectories
            copy_directory(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)  # Copy files
            print(f"Copied: {dest_path}")


def extract_title(markdown):
    """Extracts the first H1 title from markdown."""
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 title found in markdown")


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    """Recursively generate pages for all markdown files in a directory."""
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(
                    dest_dir_path, os.path.splitext(relative_path)[0] + ".html")

                # Create the destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Generate the HTML page
                generate_page(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    """Generates an HTML page using markdown and a template."""

    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    output_content = template_content.replace(
        "{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(output_content)


def main():
    template_path = "template.html"
    src = "static"
    dest = "public"

    # function deletes public folder contents before copying
    copy_directory(src, dest)

    # Generate all pages recursively from the content directory
    generate_pages_recursive("content", template_path, "public")


if __name__ == "__main__":
    main()
