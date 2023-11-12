import constants
import csv
import bs4
import typing
from bs4 import BeautifulSoup

# for handling strange date time, reference: https://stackoverflow.com/questions/30337528/make-beautifulsoup-handle-line-breaks-as-a-browser-would
def get_text(tag: bs4.Tag) -> str:
    _inline_elements = {"a","span","em","strong","u","i","font","mark","label",
    "s","sub","sup","tt","bdo","button","cite","del","b","a","font",}

    def _get_text(tag: bs4.Tag) -> typing.Generator:
        for child in tag.children:
            if isinstance(child, bs4.Tag):
                # if the tag is a block type tag then yield new lines before after
                # is_block_element = child.name not in _inline_elements
                # if is_block_element:
                #     yield "\n"
                yield from ["\n"] if child.name == "br" else _get_text(child)
                # if is_block_element:
                #     yield "\n"
            elif isinstance(child, bs4.NavigableString):
                yield child.string

    return "".join(_get_text(tag))

def get_subjects(driver, root_dir):
    driver.get(root_dir)
    driver.maximize_window()
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    subject_div = soup.find("div", {"class": "depts"})

    subjects = []
    for item in subject_div: subjects.append(item.text)
    return subjects

def get_info(driver, page_dir, writer):
    driver.get(page_dir)
    driver.maximize_window()
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')

    classes_div = soup.find("div", {"id": "classes"})
    for course_div in classes_div:
        subject_title_element = course_div.find("h2")
        if subject_title_element == -1: continue
        else:
            subject_title = subject_title_element.text
            title = subject_title.split(" - ")[0]
            table = course_div.find("table", {"class": "sections"})
            rows = table.find("tbody").find_all("tr")

            is_title = True

            # handle the case of multiple rows for a section
            prev_section = ""
            prev_enrollment = 0  

            for row in rows:
                # skip the first row, which is a title
                if is_title:
                    is_title = False
                    continue

                cells = row.find_all("td")
                if len(cells) > constants.NORMAL_ENROLLED_POS + 1:
                    section = (cells[constants.NORMAL_SECTION_POS].text).split(" ")[0]
                    prev_section = section

                    class_time = get_text(cells[constants.NORMAL_TIME_POS])

                    class_location = cells[constants.NORMAL_LOCATION_POS].text

                    class_enrollment = cells[constants.NORMAL_ENROLLED_POS].text
                    prev_enrollment = class_enrollment
                else:
                    # skip the row for the varying location and time slot for the same course for simplcity
                    class_time = get_text(cells[constants.SPECIAL_TIME_POS])
                    if constants.NEW_LINE in class_time: continue

                    section = prev_section
                    class_enrollment = prev_enrollment
                    
                    class_location = cells[constants.SPECIAL_LOCATION_POS].text

                # extract the location group
                splitted_location = class_location.split(", ")
                location_classification = ""
                if len(splitted_location) == 1: location_classification = class_location.split(" (")[0]
                else: location_classification = splitted_location[1].split(" (")[0]

                # extract the day (Mon - Sun) of the time
                day = ""
                if constants.NEW_LINE in class_time:
                    day = (class_time.split(constants.NEW_LINE)[1]).split(" ")[0]
                else:
                    day = class_time.split(" ")[0]

                # print(f"Section: {section}, time: {class_time}, location: {class_location}, enrollment: {class_enrollment}, classification: {location_classification}, day: {day}")
                writer.writerow([title, section, class_time, class_location, class_enrollment, location_classification, day])

    print(f"Completed scraping for {page_dir}")
