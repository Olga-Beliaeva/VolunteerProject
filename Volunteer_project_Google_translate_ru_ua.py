
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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

url = 'https://translate.google.com/?sl=ru&tl=uk&op=translate'

def from_ru_to_ua(name: str) -> str:
    """
    return a name translated (transliterated) to ua
    """
    name = name.lower()
    try:
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as browser:
            browser.get(url)
            browser.find_element(By.XPATH, '//textarea[@aria-label="Исходный текст"]').send_keys(name)
            time.sleep(2)
            # to reach out a blocked part we need to scroll a page down
            browser.execute_script("window.scrollTo(500,0)")
            time.sleep(2)
            translated = browser.find_element(By.XPATH, '//span[@class="ryNqvb"]').text
            print(f'Google: translation for {name} in progress...')
            return translated
    except Exception as e:
        # print(e)
        return f'Google: translation for {name} is not available at the moment'


if __name__ == '__main__':
    # any data provided in Test is random and can not match with any personal information
    TEST = [
        'Савельев Артур Юрьевич',
        'Самарский Игорь Эдуардович'
    ]
    for name in TEST:
        print(from_ru_to_ua(name))
