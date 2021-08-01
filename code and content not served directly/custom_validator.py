import glob, os
from bs4 import BeautifulSoup

"""
validates my website for some things that I want to check

including custom stuff specific to only that site
"""


def main():
    os.chdir("../")
    for filename in glob.glob("**/*.html", recursive=True):
        if filename.find("code and content not served directly") != 0:
            validate_html(filename)

def validate_html(filename):
    html = open(filename).read()

    if "google" in filename:
        if len(html) < 60:
            if "google-site-verification" in html:
                #print("treating", filename, "with content", html, "as ownership verification file and skipping its validation")
                return

    parsed_html = BeautifulSoup(html, "html.parser")
    require_wrapping_of_images(filename, parsed_html)
    require_favicon(filename, parsed_html)
    require_utf8_charset_declaration_and_magical_incantations_in_meta_tag(filename, parsed_html)
    require_language_to_be_specifified_as_english(filename, parsed_html)

def is_properly_handled_image(image):
    # all images should either
    # - have image_with_frame class (on img tag)
    # or
    # - be directly in div with img_container class
    classes_if_specified = image.get('class')
    if classes_if_specified != None:
        if "framed" in classes_if_specified:
            return True
        # TODO deprecate this
        if "image_with_frame" in classes_if_specified:
            return True

    if image.parent.name == "div" and "img_container" in image.parent.get('class'):
        return True

    if image.parent.name == "a":
        if image.parent.parent.name == "div" and "img_container" in image.parent.parent.get('class'):
            return True
    return False

def require_wrapping_of_images(filename, parsed_html):
    # completely custom requirement for this site
    images = parsed_html.find_all("img")
    for image in images:
        if is_properly_handled_image(image) == False:
            print("wrapping of " + str(image) + " in " + filename + " is not handled properly (should be within <div class=img_container> or with class=framed on itself")

def require_favicon(filename, parsed_html):
    head = get_singleton_tag("head", filename, parsed_html)
    if head == None:
        return
    links = head.find_all("link")
    for link in links:
        if link.get("rel")[0] == "icon":
            return
    print(filename, "has no favicon")
    print()

def require_utf8_charset_declaration_and_magical_incantations_in_meta_tag(filename, parsed_html):
    head = get_singleton_tag("head", filename, parsed_html)
    title_position = None
    meta_position = None
    position = 0
    for child in head.children:
        if(child != "\n"):
            #print(child.name)
            if child.name == "title":
                if title_position != None:
                    print(filename, 'has title set multiple times!')
                title_position = position
            if child.name == "meta":
                if meta_position != None:
                    print(filename, 'has meta set multiple times!')
                meta_position = position
            position += 1
    if title_position == None or meta_position == None:
        if title_position == None:
            print(filename, "has title not set")
        if meta_position == None:
            print(filename, "has meta not set")
    elif title_position < meta_position:
        # https://www.matuzo.at/blog/html-boilerplate/#content
        # It must come before the <title> element to avoid faulty characters in the page title.
        print(filename, 'has title before meta, it means that special characters in the title may be corrupted in some cases!')

    meta = get_singleton_tag("meta", filename, parsed_html)
    if meta == None:
        return

    tags = meta.find_all("charset")
    for entry in tags:
        if entry.get("charset")[0] != "UTF-8":
            # https://www.matuzo.at/blog/html-boilerplate/#content
            # Here’s how Safari displays my name with and without the charset meta tag.
            # Manuel Matuzović - Manuel MatuzoviÄ‡
            print(filename, 'charset must be UTF-8! Use meta tag with `charset="UTF-8"`')
            print()

    tags = meta.find_all("charset")
    for entry in tags:
        if entry.get("width")[0] != "device-width, initial-scale=1":
            # https://github.com/joshbuchea/HEAD#recommended-minimum
            # use the physical width of the device (great for mobile!)
            # disable dumb autozooming
            print(filename, 'magical viewport incantation is missing! Use meta tag with `width="device-width, initial-scale=1"`')

    tags = meta.find_all("name")
    for entry in tags:
        if entry.get("name")[0] != "viewport":
            # https://github.com/joshbuchea/HEAD#recommended-minimum
            # viewport settings related to mobile responsiveness
            print(filename, 'magical name="viewport" incantation is missing! Use meta tag with `name="viewport"`')


def require_language_to_be_specifified_as_english(filename, parsed_html):
    # https://www.matuzo.at/blog/lang-attribute/
    # https://adrianroselli.com/2015/01/on-use-of-lang-attribute.html
    # also, detected by some validator and may obscure more serious issues
    
    html = get_singleton_tag("html", filename, parsed_html)
    if html == None:
        return

    if html.get("lang") == "en":
        return
    print(filename, "language is not specified as English!", html.get("lang"))
    print()

def get_singleton_tag(tag, filename, parsed_html):
    found = parsed_html.find_all(tag)
    if(len(found) != 1):
        print(filename, "has <" + tag + ">", len(found), "times!")
    if(len(found) == 0):
        print(filename, "has no <" + tag + ">!")
        return None
    return found[0]

main()
