
"""
On some stage of the project we need to generate
a father name of a person we are checking.

A full russian name contains a derivative of a person's father name (aka otchestvo|middle name)
and we use otchestvo as a key to find out a father's name in russian_male_names.txt

this module downloads russian man names from
https://kupidonia.ru/spisok/polnyj-spisok-muzhskih-imen
into a text file in a way when a new first letter stars a new line

"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

def russian_male_names():
    with webdriver.Chrome() as browser:
        browser.get('https://kupidonia.ru/spisok/polnyj-spisok-muzhskih-imen')
        print('in progress...')

        amount = 0
        links = [
            href.find_element(By.TAG_NAME, 'a').get_attribute('href')
            for href in browser.find_elements(
                 By.XPATH,
                "//div[@class='list_alphabet_item']"
            )
        ]

        # open file to write names in
        with open('russian_male_names.txt', 'w', encoding='utf-8-sig') as file:
            # go through all pages and write all found names in the file
            for ind in range(len(links)):
                browser.get(links[ind])
                print( browser.find_element(By.TAG_NAME,'h1').text)
                file.write('\n')
                for name in browser.find_elements(By.XPATH, "//div[@class='position_title']"):
                    time.sleep(1)
                    file.write(name.text.lower())
                    file.write(' ')
                    amount += 1

                # progress bar
                percent_done = int(ind/ len(links) * 100)
                sys.stdout.write('\r[{0}] {1}%'.format('#' * int(percent_done / 5), percent_done))
                sys.stdout.flush()
                print()
            print('\nAmount of names in the file:', amount)

def main():
    print('started...')
    russian_male_names()

if __name__ == '__main__':
    main()
