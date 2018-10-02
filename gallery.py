import os
from sys import argv

import jinja2


def find_images(directory, dir_out):
    return [{"path": os.path.relpath(os.path.join(root, file), dir_out),
             "tags": os.path.normpath(os.path.relpath(root, dir_out)).split(os.path.sep),
             "file": file}
            for root, dirs, files in os.walk(directory) for file in files
            if file.endswith((".gif", ".bmp", ".jpg"))]


def render_template(images):
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("template.html")
    return template.render(images=images)


def main(dir_in, dir_out):
    with open(os.path.join(dir_out, "gallery.html"), "w") as f:
        f.write(render_template(find_images(dir_in, dir_out)))
    print("done")


if __name__ == "__main__":
    main(dir_in=argv[1], dir_out=argv[1])
