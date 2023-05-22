
"""
Volunteer.su  is a website where a Russian patriotic initiative group
collects and publishes data about military personnel, activists, etc., supporting Ukraine.

Being listed or having a close relative like father listed on this website
is likely to cause problems for an individual at the border.

This module check presence of a person and his father on Volunteer.su and
returns a list with found references or an empty list.
"""

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from Volunteer_project_Father_name import Father                      # my modul
from Volunteer_project_Google_translate_ru_ua import from_ru_to_ua    # my modul

def split_name(name:str) ->tuple:
    """
    return cleaned and split data in case
    a name presented in russian & ukrainian
    """
    regex = re.compile("[ \t]+")
    name_split = regex.sub(' ', name).split(' ')
    if len(name)==6:
        name_ru = ' '.join(name_split[:3])
        name_ua = ' '.join(name_split[3:])
        return name_ru, name_ua
    else:
        return name, ''

def volunteer(name:str) -> list:
    """
    Insert a last name in a search window and click the search button
    Find relevant name and open its link in a new window
    Find a birthday
    Gather found names, birthdays and links in a list
    Return this list
    """
    print(f'Volunteer: checking name is {name}')
    full_name = name.lower()
    short_name = re.match(r'\w+ \w+', full_name).group() if len(full_name) > 2 else full_name
    short_name_ua = from_ru_to_ua(short_name).lower()
    father_name = Father(full_name).father()

    names_cast = {full_name, short_name, father_name,  short_name_ua}

    # search by surname gives the most relevant outcome
    last_name = full_name.split()[0]

    # print(f'search for the last name {last_name} and names to check {names_cast}')

    with webdriver.Chrome() as browser:
        browser.get('https://volunteer.su/search')

        # insert a last name and click a search button
        browser.find_element(By.XPATH, "//input[@id='edit-text']").send_keys(last_name)
        browser.find_element(By.XPATH, "//input[@class='form-submit']").click()

        links = []
        pay_attention = []

        # full name is under an attribute "title", link is an attribute "href"
        # some names are presented in russian and ukrainian others in russian only
        for data in browser.find_elements(By.XPATH, "//li[@class='node-readmore first last']"):
            found_on_page = data.find_element(By.TAG_NAME, 'a').get_attribute('title').lower()

            name_found, *other_name_found = split_name(found_on_page)
            names_found = {name_found, *other_name_found}

            # check if there are some intersections between names found on Volunteer and names_cast
            shared_name = len(names_cast & names_found) !=0

            link = data.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # if there are some intersections a link goes to links list
            if shared_name:
                links.append(link)

        # only if there is some interception a new window is open by a found link
        for link in links:
            browser.execute_script(f'window.open("{link}")')
            time.sleep(1)

        tabs = browser.window_handles
        for tab in range(1, len(tabs)):
            browser.switch_to.window(browser.window_handles[tab])
            time.sleep(2)

            #a full name from an open link is found here
            name_relevant_raw = browser.find_element(By.TAG_NAME, 'head').find_element(
                                By.TAG_NAME, 'title').get_property('textContent')  # ('innerText')
            name_relevant = re.search(r'.*(?=(\|))', name_relevant_raw).group()
            try:
                # now we are looking for a birthday
                # but Volunteer info is so badly structured
                # that instead we may spot something unexpected
                info = browser.find_element(
                       By.XPATH, '//div[@class="field-items"]/div[@class="field-item even"]'
                ).text
                pay_attention.append((name_relevant, info, link))
            except Exception as e:
                print('exception', e)
                pay_attention.append((name_relevant, link))

            print(f'Volunteer: for name {name} is found {name_relevant}')
        return pay_attention


if __name__ == '__main__':
    # all test names found on Volunteer.ru for  test purpose only
    TEST = [
        #"Минаков Геннадий Петрович"
        #"Протасов Дмитрий Иванович"#,
        #"Токарев Иван Анатольевич"#,
        "Шах Андрей Витальевич"#,
        #"Панченко Кирилл Андреевич"

    ]
    for name in TEST:
        print(volunteer(name))

