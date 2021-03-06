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

def require_wrapping_of_images(parsed_html):
    # completely custom requirement for this site
    images = parsed_html.find_all("img")
    for image in images:
        if is_properly_handled_image(image) == False:
            print("wrapping of " + str(image) + " in " + filename + " is not handled properly")

def require_favicon(parsed_html):
    head = parsed_html.find_all("head")
    if(len(head) != 1):
        print(filename, "has <head>", len(head), "times!")
    if(len(head) == 0):
        return
    links = head[0].find_all("link")
    for link in links:
        if link.get("rel")[0] == "icon":
            return
    print(filename, "has no favicon")
    print()

def require_language_to_be_specifified_as_english(parsed_html):
    # https://www.matuzo.at/blog/lang-attribute/
    # https://adrianroselli.com/2015/01/on-use-of-lang-attribute.html
    # also, detected by some validator and may obscure more serious issues
    
    html = parsed_html.find_all("html")
    if(len(html) != 1):
        print(filename, "has <html>", len(head), "times!")
    if(len(html) == 0):
        return
    if html[0].get("lang") == "en":
        return
    print(filename, "language is not specified as English!", html[0].get("lang"))
    print()

def validate_html(filename):
    html = open(filename).read()

    if "google" in filename:
        if len(html) < 60:
            if "google-site-verification" in html:
                print("treating", filename, "with content", html, "as ownership verification file and skipping its validation")
                return

    parsed_html = BeautifulSoup(html, "html.parser")
    require_wrapping_of_images(parsed_html)
    require_favicon(parsed_html)
    require_language_to_be_specifified_as_english(parsed_html)

os.chdir("../")
for filename in glob.glob("**/*.html", recursive=True):
    validate_html(filename)
