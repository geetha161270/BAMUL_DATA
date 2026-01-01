import os
import shutil

def copy_first_image_to_dashboard3_public(
    folder_name: "task1",
    base_path: "D:\task1"
) -> str | None:
    """
    Copies the first image from the given folder into
    dashboard3 public/files directory, renaming it to folder_name.ext
    """

    IMAGE_EXTS = (".png")

    SOURCE_FOLDER = os.path.join(base_path, folder_name)
    DEST_FOLDER =" D:\common folder"
    if not os.path.isdir(SOURCE_FOLDER):
        raise FileNotFoundError(f"Source folder not found: {SOURCE_FOLDER}")

    if not os.path.isdir(DEST_FOLDER):
        raise FileNotFoundError(f"Destination folder not found: {DEST_FOLDER}")

    images = sorted(
        f for f in os.listdir(SOURCE_FOLDER)
        if f.lower().endswith(IMAGE_EXTS)
    )

    if not images:
        return None

    src_image = os.path.join(SOURCE_FOLDER, images[0])

    # Preserve original extension
    _, ext = os.path.splitext(images[0])
    new_filename = f"{folder_name}{ext.lower()}"

    dest_image = os.path.join(DEST_FOLDER, new_filename)

    shutil.copy2(src_image, dest_image)

    return dest_image