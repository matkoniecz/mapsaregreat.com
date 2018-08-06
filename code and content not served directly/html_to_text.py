import glob, os
from bs4 import BeautifulSoup

os.chdir("../")
for filename in glob.glob("**/*.html", recursive=True):
    print(BeautifulSoup(open(filename).read(), "html.parser").get_text())
