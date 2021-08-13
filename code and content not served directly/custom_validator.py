import glob, os
from bs4 import BeautifulSoup

"""
validates my website for some things that I want to check

including custom stuff specific to only that site
"""


def main():
    os.chdir("../")
    os.system("rm 'code and content not served directly/linkchecker_data.csv'")
    os.system("linkchecker index.html --verbose -o csv > 'code and content not served directly/linkchecker_data.csv' 2>/dev/null")
    # --check-extern would also check external links but it would be much slower and repetetive running may be not entirely OK...
    # entire stderr is redirected to /dev/null due to https://github.com/linkchecker/linkchecker/issues/552
    for filepath in glob.glob("**/*.html", recursive=True):
        if filepath.find("code and content not served directly") != 0:
            validate_html(filepath)

def validate_html(filepath):
    html = open(filepath).read()

    if "google" in filepath:
        if len(html) < 60:
            if "google-site-verification" in html:
                #print("treating", filepath, "with content", html, "as ownership verification file and skipping its validation")
                return

    parsed_html = BeautifulSoup(html, "html.parser")
    require_wrapping_of_images(filepath, parsed_html)
    require_existence_of_images(filepath, parsed_html)
    require_favicon(filepath, parsed_html)
    require_utf8_charset_declaration_and_magical_incantations_in_meta_tag(filepath, parsed_html)
    require_language_to_be_specifified_as_english(filepath, parsed_html)
    require_using_canonical_css(filepath, parsed_html)

def is_properly_wrapped_image(image):
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

def require_wrapping_of_images(filepath, parsed_html):
    # completely custom requirement for this site
    images = parsed_html.find_all("img")
    for image in images:
        if is_properly_wrapped_image(image) == False:
            print("wrapping of " + str(image) + " in " + filepath + " is not handled properly (should be within <div class=img_container> or with class=framed on itself")

def require_favicon(filepath, parsed_html):
    head = get_singleton_tag("head", filepath, parsed_html)
    if head == None:
        return
    links = head.find_all("link")
    for link in links:
        if link.get("rel")[0] == "icon":
            if is_file_existing(filepath, link.get("href")) == False:
                    print(filepath, "links nonexisting favicon file")
            return
    print(filepath, "has no favicon")
    print()

def require_existence_of_images(filepath, parsed_html):
    images = parsed_html.find_all("img")
    for image in images:
        if is_file_existing(filepath, image.get("src")) == False:
                print(filepath, "links nonexisting image in", image)

def require_using_canonical_css(filepath, parsed_html):
    head = get_singleton_tag("head", filepath, parsed_html)
    if head == None:
        return
    links = head.find_all("link")
    for link in links:
        if link.get("rel")[0] == "stylesheet":
            if link.get("href") == "https://mapsaregreat.com/style.css":
                # yeah that is my custom validator, and it is canonical
                # css for me
                return
            if is_file_existing(filepath, link.get("href")) == False:
                print(filepath, "links nonexisting CSS")
            if link.get("href") != "style.css":
                    print(filepath, "has unusal css link", link.get("href"))
            return
    print(filepath, "has no stylesheets declared!")
    print()

def is_file_existing(filepath, file_source):
    """
    filepath - path to file containing given path.
    Path is from the repository root, see main()

    file_source - path, possibly relative
    """
    directory_location = os.path.dirname(filepath)
    target = os.path.join(directory_location, file_source)
    if(os.path.isfile(target)):
        return True

    print("==============")
    print(filepath)
    print(file_source)
    print(directory_location)
    print(target)
    print("==============")

    return False

def require_utf8_charset_declaration_and_magical_incantations_in_meta_tag(filepath, parsed_html):
    head = get_singleton_tag("head", filepath, parsed_html)
    title_position = None
    meta_position = None
    noscript = None
    position = 0
    for child in head.children:
        if(child != "\n"):
            #print(child.name)
            if child.name == "title":
                if title_position != None:
                    print(filepath, 'has title set multiple times!')
                title_position = position
            if child.name == "meta":
                if meta_position != None:
                    print(filepath, 'has meta set multiple times!')
                meta_position = position
            if child.name == "noscript":
                noscript = child
            position += 1
    if title_position == None or meta_position == None:
        if title_position == None:
            print(filepath, "has title not set")
        if meta_position == None:
            if noscript != None:
                for child in noscript.children:
                    if child.name == "meta":
                        if child.get("http-equiv") == "refresh":
                            if child.get("content") != None:
                                # redirect page, skipping this check
                                return
            print(filepath, "has meta not set")
    elif title_position < meta_position:
        # https://www.matuzo.at/blog/html-boilerplate/#content
        # It must come before the <title> element to avoid faulty characters in the page title.
        print(filepath, 'has title before meta, it means that special characters in the title may be corrupted in some cases!')

    meta = get_singleton_tag("meta", filepath, parsed_html)
    if meta == None:
        return

    tags = meta.find_all("charset")
    for entry in tags:
        if entry.get("charset")[0] != "UTF-8":
            # https://www.matuzo.at/blog/html-boilerplate/#content
            # Here’s how Safari displays my name with and without the charset meta tag.
            # Manuel Matuzović - Manuel MatuzoviÄ‡
            print(filepath, 'charset must be UTF-8! Use meta tag with `charset="UTF-8"`')
            print()

    tags = meta.find_all("charset")
    for entry in tags:
        if entry.get("width")[0] != "device-width, initial-scale=1":
            # https://github.com/joshbuchea/HEAD#recommended-minimum
            # use the physical width of the device (great for mobile!)
            # disable dumb autozooming
            print(filepath, 'magical viewport incantation is missing! Use meta tag with `width="device-width, initial-scale=1"`')

    tags = meta.find_all("name")
    for entry in tags:
        if entry.get("name")[0] != "viewport":
            # https://github.com/joshbuchea/HEAD#recommended-minimum
            # viewport settings related to mobile responsiveness
            print(filepath, 'magical name="viewport" incantation is missing! Use meta tag with `name="viewport"`')


def require_language_to_be_specifified_as_english(filepath, parsed_html):
    # https://www.matuzo.at/blog/lang-attribute/
    # https://adrianroselli.com/2015/01/on-use-of-lang-attribute.html
    # also, detected by some validator and may obscure more serious issues
    
    html = get_singleton_tag("html", filepath, parsed_html)
    if html == None:
        return

    if html.get("lang") == "en":
        return
    print(filepath, "language is not specified as English!", html.get("lang"))
    print()

def get_singleton_tag(tag, filepath, parsed_html):
    found = parsed_html.find_all(tag)
    if(len(found) != 1):
        print(filepath, "has <" + tag + ">", len(found), "times!")
    if(len(found) == 0):
        print(filepath, "has no <" + tag + ">!")
        return None
    return found[0]

main()
