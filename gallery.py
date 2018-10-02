import os
from sys import argv

import jinja2

dir_in = argv[1]
dir_out = argv[1]

images = list()
for root, subdirs, files in os.walk(dir_in):
    for file in files:
        if file.endswith((".gif", ".bmp", ".jpg")):
            image = {"path": os.path.relpath(os.path.join(root, file), dir_out),
                     "tags": os.path.normpath(os.path.relpath(root, dir_out)).split(os.path.sep),
                     "file": file}
            images.append(image)

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(images=images)  # this is where to put args to the template renderer

with open(os.path.join(dir_out, "gallery.html"), "w") as f:
    f.write(outputText)
print("done")
