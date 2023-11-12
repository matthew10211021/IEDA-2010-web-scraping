from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def set_driver_configs(browser: str):
    """Returns the corresponding selenium web driver. Currently only supports Chrome and Edge."""
    if (browser == 'Chrome'):
        option = webdriver.ChromeOptions()
        option.add_argument("--headless=new")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    elif (browser == 'Edge'):
        option = webdriver.EdgeOptions()
        option.add_argument("--headless=new")
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=option)
    return driver

