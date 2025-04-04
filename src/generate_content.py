from genericpath import isfile
import os
import shutil
from convert import extract_title, markdown_to_html_node


PUBLIC_FOLDER_PATH = "./docs/"
SOURCE_FOLDER = "./static/"
TEMPLATE_PATH = "./template.html"
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


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
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
    page = page.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    new_html_page_file = open(dest_path, "x")
    new_html_page_file.write(page)
    new_html_page_file.close()

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):
    files = os.listdir(dir_path_content)
    
    for file in files:
        source_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)

        if os.path.isfile(source_path):            
            html_file_name = file.replace("md", "html")

            dest_path = os.path.join(dest_dir_path, html_file_name)
            generate_page(source_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(source_path, template_path, dest_path, basepath)



