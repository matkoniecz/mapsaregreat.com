# this file is licenced under CC0

# instructions for Linux using Firefox
# download Geckodriver binary - https://github.com/mozilla/geckodriver/releases
# put it somewhere where $PATH will find it
# good documentations is at https://selenium-python.readthedocs.io/

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import inspect

screenshot_width = 1024
screenshot_height_standard = 768
screenshot_height_small = 400

# as recommended on http://selenium-python.readthedocs.io/waits.html#explicit-waits
def smart_overpass_capture(url, image_file, driver):
    driver.get(url)
    element = WebDriverWait(driver, 10).until_not(
        EC.presence_of_element_located((By.CLASS_NAME, "loading"))
        #EC.presence_of_element_located((By.ID, "aborter")) # requires additional sleep to avoid capturing "rendering geojson" stage
    )
    driver.save_screenshot(image_file)

firefox_options = webdriver.FirefoxOptions()
# in production mode headless is likely to be preferrable
# firefox_options.set_headless()
driver = webdriver.Firefox(firefox_options=firefox_options)

# recommended by https://stackoverflow.com/a/31867043/4130619
os.chdir(os.path.dirname(os.path.abspath(inspect.stack()[0][1])))
print(os.path.dirname(os.path.abspath(inspect.stack()[0][1])))
os.chdir("../geographic-data-mining-and-visualisation-for-beginners")

# supposedly captures entire page or its part, untested
# firefox_elem = firefox_driver.find_element_by_tag_name('html')
# firefox_elem.screenshot(<png_screenshot_file_path>)

# may capture too early - then it will show stage vefore query completed
# may capture too late and crash as apparently there will be nothing to capture
"""
driver.get('http://overpass-turbo.eu/s/zMi')
time.sleep(5)
driver.save_screenshot("hamm-playgrounds.png")
"""
driver.set_window_size(screenshot_width, screenshot_height_small)
driver.get('https://duckduckgo.com/?q=wetland+OSM+Wiki&ia=web')
driver.save_screenshot('wetland-search-results.png')

driver.set_window_size(screenshot_width, screenshot_height_standard)
driver.get('https://www.openstreetmap.org/#map=10/54.2066/-4.5782')

#hide banners about SOtM and other spam
for popup in driver.find_elements_by_class_name("close-wrap"):
    popup.click()
driver.save_screenshot('Isle-of-Man.png')

#try saving just map, without interface
#for further cleaning up see
#https://stackoverflow.com/questions/17911980/selenium-with-python-how-to-modify-an-element-css-style
#https://selenium-python.readthedocs.io/faq.html#how-to-scroll-down-to-the-bottom-of-a-page
#https://stackoverflow.com/questions/35922259/modify-innerhtml-using-selenium
#element = driver.find_element_by_id('map')
#element.screenshot('test.png')

driver.set_window_size(screenshot_width, screenshot_height_standard)
smart_overpass_capture('http://overpass-turbo.eu/s/zMi', "Hamm-playgrounds.png", driver)
smart_overpass_capture('http://overpass-turbo.eu/s/zMQ', "Kampong_Ayer-everything.png", driver)
smart_overpass_capture('http://overpass-turbo.eu/s/zNL', "Nepal-glaciers.png", driver)
smart_overpass_capture('http://overpass-turbo.eu/s/Acj', "Hawaii-volcanoes.png", driver)

driver.quit()