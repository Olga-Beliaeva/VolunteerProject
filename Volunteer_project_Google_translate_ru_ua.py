
"""
On some stage of the project we need to translate a name of a person we are checking in Ukrainian.
In real process we use DeepL API for this purpose.
But we expect you don't have an account on https://www.deepl.com/.
And for demonstration purpose we have replaced DeepL API by Google.
Google protects itself by Cloudflare.
Google translation service returns only the first entrance request,
but it is enough to demonstrate this module.
Module returns whether a translated name or an exception phrase.
"""

import time
from selenium.webdriver.common.by import By
# pip install undetected-chromedriver
import undetected_chromedriver as uc


url = 'https://translate.google.com/?sl=ru&tl=uk&op=translate'

def from_ru_to_ua(name:str) -> str:
    """
    return a name translated (transliterated) to ua
    """
    name = name.lower()
    try:
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        browser = uc.Chrome(use_subprocess=True, options=options)
        browser.get(url)
        browser.find_element(By.XPATH, '//textarea[@aria-label="Исходный текст"]').send_keys(name)
        time.sleep(2)
        # to reach out a blocked part we need to scroll a page down
        browser.execute_script("window.scrollTo(500,0)")
        time.sleep(2)
        translated = browser.find_element(By.XPATH, '//span[@class="ryNqvb"]').text
        print('Google: name translation from ru to ua in progress...')
        browser.close()
        return translated
    except Exception as e:
        # print(e)
        return f'Google: translation for {name} is not available at the moment'


if __name__ == '__main__':
    # any data provided in Test is random and can not match with any personal information
    TEST = [
        # "Савельєв",
        # "Савельев",
        'Савельев Артур Юрьевич',
        'Самарский Игорь Эдуардович'
    ]
    for name in TEST:
        print(from_ru_to_ua(name))



