import glob, os
from bs4 import BeautifulSoup

"""
validates my website for some things that I want to check

including custom stuff specific to only that site
"""

def is_properly_handled_image(image):
    # all images should either
    # - have image_with_frame class (on img tag)
    # or
    # - be directly in div with img_container class
    classes_if_specified = image.get('class')
    if classes_if_specified != None:
        if "image_with_frame" in classes_if_specified:
            return True

    if image.parent.name == "div" and "img_container" in image.parent.get('class'):
        return True

    if image.parent.name == "a":
        if image.parent.parent.name == "div" and "img_container" in image.parent.parent.get('class'):
            return True
    return False

def validate_html(filename):
    html = open(filename).read()
    bs = BeautifulSoup(html, "html.parser")
    images = bs.find_all("img")
    for image in images:
        if is_properly_handled_image(image) == False:
            print("wrapping of " + str(image) + " in " + filename + " is not handled properly")

os.chdir("../")
for filename in glob.glob("**/*.html", recursive=True):
    validate_html(filename)
