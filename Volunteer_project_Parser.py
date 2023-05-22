
"""
This module filters data* by provided fields,
clears data by templates and returns data in expected format.

(*) incoming data is in russian language
"""

import re

# return date in dd.mm.yyyy
# replacing any of (:;/,_-) by .
def replace_by_dot(func):
    def wrapper(*args, **kwargs):
        to_replace = func(*args, **kwargs)
        replaced = []
        regex = re.compile("[:;/,_-]+")
        for date in to_replace:
            result = regex.sub('.', date)
            replaced.append(result)
        return replaced
    return wrapper

class Parser:

    regEx_dict = {
        'birthday': re.compile(r' (\d{1,2})(.\d{2}.| \w+ )(\d{2,4})'),
        'names': re.compile(r'[А-Я][^У ]\w+.[А-Я]\w+.[А-Я]\w+'),
        'number': re.compile(r'(eu.{,1}\d{,4}|заявка \d{,4})'),
        'link': re.compile(r'\w{5}://[p]\S+'),
        'contacts': re.compile(r'[@|+]\w*'),
        'digits': re.compile(r'\d+')
    }

    month_dict = {
        'янв': '.01.', 'фев': '.02.', 'мар': '.03.', 'апр': '.04.',
        'мая': '.05.', 'июн': '.06.', 'июл': '.07.', 'авг': '.08.',
        'сен': '.09.', 'окт': '.10.', 'ноя': '.11.', 'дек': '.12.'
    }

    def __init__(self, texts:str):
        self._texts = texts.replace('ё', 'е')

    def parser(self, regEx:str, txt:str=None) -> list:
        """
        filter data with given regular exp
        return list of filtered data or empty (technically with '') list
        """
        text = self._texts if txt==None else txt
        parsed = self.regEx_dict[regEx].findall(text)
        parsed = parsed if len(parsed) > 0 else ['']
        return parsed

    @replace_by_dot
    def birthday(self, date_list:list) -> list:
        """
        a birthday might be provided in any legit format
        we need to format it in dd.mm.yyyy that accepted by
        #Volunteer.ru
        return a date in the dd.mm.yyyy format
        """
        dates = []
        for date in date_list:
            if date != '':
                d, m, y = date
                #  check procedure is provided for men 16 - 65 y.o.
                #  min year of birth for checking is 2007
                #  if a year provided in a yy form we convert it if 2000 - 2007
                #  for 00 - 07 in 19.. otherwise:
                #  00 -> 2000, 07 -> 2007 (16 y.o)
                try:
                    m = self.month_dict[m.strip()[:3]] if m.strip().isalpha() else m
                    d = d if len(d) == 2 else f'0{d}'
                    y = y if len(y) == 4 else f'19{y}' if int(y) > 7 else f'20{y}'
                    dates.append((d + m + y))
                except: dates.append('')
            else:
                dates.append('')
        return dates

    def contact(self, contact_list:list) -> list:
        """
        return contact in @ or https://t.me/ format
        """
        contacts = []
        for cont in contact_list:
            if cont != '':
                cont = cont if cont[0] == '@' else 'https://t.me/' + cont
                contacts.append(cont)
            else: contacts.append('')
        return contacts

    def short_name(self, full_name):
        """
        return a short name (last + first names)
        provided from a full name (last + first + father names)
        """
        try:
            last_name, first_name, *args = full_name.split()
            return last_name + ' ' + first_name
        except: return ''


if __name__ == '__main__':
    # any data provided in Test is random and can not match with any personal information
    TEST = [
        "2891 https://ss.korostel.one/?p=829851391  eu 28 Залов Александр Валентинович 1-03-1962 г, р., г. Мариуполь +381232342323",
        "  Каров Владимир Иванович 9 февраля 1988 г.Новая Каховка https://ss.korostel.one/?p=829851399   Онищенко Дмитрий Сергеевич , дата рождения: 25/08.2004 Заявка 29 @hhhhhh",
    ]
    for line in TEST:
        data = Parser(line)
        app_num = data.parser('number', line.lower())
        num = app_num[0] if len(app_num) > 0 else ''
        contacts = data.parser('contacts')
        birthdays = data.parser('birthday')

        print([
            data.parser('digits', num), data.parser('names'),
            data.birthday(birthdays), data.contact(contacts),
            data.parser('link')])




