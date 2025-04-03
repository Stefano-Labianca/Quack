import os
from generate_content import (
    CONTENT_FOLDER_PATH, PUBLIC_FOLDER_PATH, TEMPLATE_PAHT, 
    copy_from_static_folder,  create_public_folder, 
    generate_page, remove_public_folder
)


def main():
    remove_public_folder()
    create_public_folder()

    if not os.path.exists(PUBLIC_FOLDER_PATH):
        raise FileNotFoundError(f"{PUBLIC_FOLDER_PATH} not found")
    
    copy_from_static_folder()
    print("\n ------ Start Generation ------")
    generate_page( 
        os.path.join(CONTENT_FOLDER_PATH, "index.md"),
        TEMPLATE_PAHT,
        os.path.join(PUBLIC_FOLDER_PATH, "index.html")
    )

main()