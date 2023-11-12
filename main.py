import csv
import config
from  scraper import *
import constants

if __name__ == "__main__":
    browser = "Chrome"
    driver = config.set_driver_configs(browser)

    with open(f"{constants.EXPORT_DIR}/{constants.FILE_NAME}", 'w', newline = '') as f:
        # overwrite the target file (if exist) and add header
        writer = csv.writer(f)
        writer.writerow(constants.HEADER)
    
        subjects = get_subjects(driver, constants.ROOT)
        for subject in subjects: get_info(driver, f"{constants.ROOT}subject/{subject}", writer)