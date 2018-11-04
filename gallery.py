import os
import re
from glob import glob
from sys import argv

import jinja2


def main(directory):
    generate_galleries_recursively(directory)
    print("done")


def generate_galleries_recursively(dir_in):
    cleanup(dir_in)
    generate_gallery(dir_in)
    for root, dirs, files in os.walk(dir_in):
        for directory in dirs:
            path = os.path.join(root, directory)
            cleanup(path)
            generate_gallery(path)


def cleanup(path):
    old_version_file = os.path.join(path, "gallery.html")
    if os.path.exists(old_version_file):
        os.remove(old_version_file)
    for f in os.listdir(path):
        if re.search(r"^gallery_(\d)+\.html$", f):
            os.remove(os.path.join(path, f))


def generate_gallery(directory, images_per_page=10):
    print(f"generating gallery for {directory}")
    images = find_images(directory, directory)
    top_level = not os.path.exists(os.path.join(directory, os.pardir, "gallery_1.html"))
    image_groups = [images[x:x + images_per_page] for x in range(0, len(images), images_per_page)]
    pages = range(1, len(image_groups) + 1)
    for page_number, image_group in zip(pages, image_groups):
        with open(os.path.join(directory, f"gallery_{page_number}.html"),
                  "w") as f:
            f.write(render_gallery(os.path.basename(directory), image_group, page_number, pages, top_level,
                                   subdirectories=list_subdirectories(directory)))


def find_images(directory, dir_out):
    return [{"path": os.path.relpath(os.path.join(root, file), dir_out),
             "tags": os.path.normpath(os.path.relpath(root, dir_out)).split(os.path.sep),
             "file": file}
            for root, dirs, files in os.walk(directory) for file in files
            if file.endswith((".gif", ".bmp", ".jpg"))]


def list_subdirectories(directory):
    return [os.path.relpath(subdir, directory) for subdir in glob(directory + "/*/")]


def render_gallery(title, images, page_number=None, pages=[], top_level=True, updirectories=None, subdirectories=None):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("template.html")
    return template.render(title=title, images=images, page_number=page_number, pages=pages, top_level=top_level,
                           updirectories=updirectories, subdirectories=subdirectories)


if __name__ == "__main__":
    main(directory=argv[1])
