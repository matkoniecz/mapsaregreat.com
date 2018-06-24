# this file is licenced under CC0 (or it is public domain anyway if content is not considered as copyrightable)

# instructions for Linux using Firefox
# download Geckodriver binary - https://github.com/mozilla/geckodriver/releases
# put it somewhere where $PATH will find it

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# as recommended on http://selenium-python.readthedocs.io/waits.html#explicit-waits
def smart_overpass_capture(url, image_file, driver):
    driver.get(url)
    element = WebDriverWait(driver, 10).until_not(
        EC.presence_of_element_located((By.CLASS_NAME, "loading"))
        #EC.presence_of_element_located((By.ID, "aborter")) # requires additonal sleep to avoid capturing "rendering geojson" stage
    )
    driver.save_screenshot(image_file)

firefox_options = webdriver.FirefoxOptions()
# in production mode headless is likely to be preferrable
# firefox_options.set_headless()
driver = webdriver.Firefox(firefox_options=firefox_options)

# supposedly captures entire page or its part, untested
# firefox_elem = firefox_driver.find_element_by_tag_name('html')
# firefox_elem.screenshot(<png_screenshot_file_path>)

# may capture too early - then it will show stage vefore query completed
# may capture too late and crash as apparently there will be nothing to capture
"""
driver.get('http://overpass-turbo.eu/s/zMi')
time.sleep(5)
driver.save_screenshot("hamm_playgrounds.png")
"""
driver.set_window_size(1024, 400)
driver.get('https://duckduckgo.com/?q=wetland+OSM+Wiki&ia=web')
driver.save_screenshot('wetland_search_results.png')

try:
    driver.set_window_size(1024, 768)
    smart_overpass_capture('http://overpass-turbo.eu/s/zMi', "Hamm_-_playgrounds.png", driver)
    smart_overpass_capture('http://overpass-turbo.eu/s/zMQ', "Kampong_Ayer_-_everything.png", driver)
    smart_overpass_capture('http://overpass-turbo.eu/s/zNL', "Nepal_-_glaciers.png", driver)
finally:
    driver.quit()
