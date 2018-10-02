import os
from glob import glob
from sys import argv

import jinja2


def main(directory):
    generate_galleries_recursively(directory)
    print("done")


def generate_galleries_recursively(dir_in):
    generate_gallery(dir_in)
    for root, dirs, files in os.walk(dir_in):
        for directory in dirs:
            generate_gallery(os.path.join(root, directory))


def generate_gallery(directory):
    print(f"generating gallery for {directory}")
    with open(os.path.join(directory, "gallery.html"), "w") as f:
        f.write(render_gallery(find_images(directory, directory), subdirectories=list_subdirectories(directory)))


def find_images(directory, dir_out):
    return [{"path": os.path.relpath(os.path.join(root, file), dir_out),
             "tags": os.path.normpath(os.path.relpath(root, dir_out)).split(os.path.sep),
             "file": file}
            for root, dirs, files in os.walk(directory) for file in files
            if file.endswith((".gif", ".bmp", ".jpg"))]


def list_subdirectories(directory):
    return [os.path.relpath(subdir, directory) for subdir in glob(directory + "/*/")]


def render_gallery(images, subdirectories):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("template.html")
    return template.render(images=images, subdirectories=subdirectories)


if __name__ == "__main__":
    main(directory=argv[1])
