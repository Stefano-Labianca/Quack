import os
import shutil
from convert import extract_title, markdown_to_html_node


PUBLIC_FOLDER_PATH = "./public/"
SOURCE_FOLDER = "./static/"
TEMPLATE_PAHT = "./template.html"
CONTENT_FOLDER_PATH = "./content/"

def create_public_folder():
    os.mkdir(PUBLIC_FOLDER_PATH)


def remove_public_folder():
    if not os.path.exists(PUBLIC_FOLDER_PATH):
        return
    
    shutil.rmtree(PUBLIC_FOLDER_PATH)


def copy_from_static_folder(start: str = SOURCE_FOLDER):
    print(f"Current Path: '{start}'")
    files = os.listdir(start)
    folders = []

    if len(files) == 0:
        return

    for file in files:
        src_file_path = os.path.join(start, file)
        base_dest_path = start.replace(SOURCE_FOLDER, "")
        dest_file_path = os.path.join(os.path.join(PUBLIC_FOLDER_PATH, base_dest_path), file)

        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path, dest_file_path)

            print(f"\t{src_file_path} moved to {dest_file_path}")
        else:
            folders.append(file)

    for folder in folders:
        src_file_path = os.path.join(start, folder)
        base_dest_path = start.replace(SOURCE_FOLDER, "")
        dest_file_path = os.path.join(os.path.join(PUBLIC_FOLDER_PATH, base_dest_path), folder)

        os.mkdir(dest_file_path)
        print()
        copy_from_static_folder(src_file_path)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path)
    md_content = md_file.read()
    md_file.close()

    template_file = open(template_path)
    template_content = template_file.read()
    template_file.close()

    root = markdown_to_html_node(md_content)
    generated_html = root.to_html()
    page_title = extract_title(md_content)

    page = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", generated_html)
    # base_dir = os.path.dirname(dest_path)

    new_html_page_file = open(dest_path, "x")
    new_html_page_file.write(page)
    new_html_page_file.close()