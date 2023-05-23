
"""
On some stage of the project we need to generate
a father name of a person we are checking.

A full russian name contains a derivative of a person's father name (aka otchestvo|middle name)
and we use otchestvo as a key to find out a name it is provided from in russian_male_names.txt

This module returns a father's name provided from a person's middle name
"""

import re

class Father:

    def __init__(self, text:str):
        self._text = text.lower().replace('ё', 'е')

    def _tokinize(self) -> list:
        """
        return name tokens
        *** info ***
        a russian full name has a structure as following
        surname + first name + a derivative from a person's father name (aka *otchestvo)
        """
        return self._text.split()

    def father(self) -> str:
        """
        open a file with common russian men names
        find a father's name matching with *otchestvo
        return person's father surname + first name
        """
        surname, _, father_name_raw, *args = self._tokinize()

        with open('russian_male_names.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

            # to speed up searching though the names file first, we launch
            # a russian_male_names-dependant dict where key is an alphabet letter and
            # value is a number of this letter in alphabet
            letters_dict = {line[1][0]:line[0] for line in list(zip(range(len(lines)), lines))}

            # second, we extract the first letter of the
            first_letter = father_name_raw[0]

            # basically a father's name and otchestvo share the same linguistic root
            # which we get by cutting otchectvo of its tail;
            # but this is a naive way to get a father's name
            # and two close names Aleksey and Aleksandr can not be distinguished without help
            father_name_base = father_name_raw[:-5] if father_name_raw != 'алексеевич' else 'алексей'

            # by the pair {first letter:number} in dict we find
            # a line to search the father name by father_name_base,
            # in case there is nothing found we just return ''
            try:
                letter_line = lines[letters_dict[first_letter]]
                s = re.search(father_name_base, letter_line).start()
                end = re.compile(r'\w+( |'')')
                f = end.search(letter_line[s:]).end()
                father_name = letter_line[s:s+f]
                return surname+' '+father_name.rstrip()
            except Exception:
                return ''


    def name(self) -> str:
        """
        return full name
        """
        surname, father, first_name, *args = self._tokinize()
        return surname+' '+father+' '+first_name


if __name__ == '__main__':
    print('Terminal: Running Volunteer_project_Father_name.py')
    # any data provided in Test is random and can not match with any personal information
    Test = [
        'Крайник Александр Михайлович',
        'Бут Александр Дмитриевич Иванов Иван Иванович',
        'Гаценкоd Леонид Алексеевич'
    ]
    for name in Test:
        person = Father(name)
        father_name = person.father()
        full_name = person.name()

        _technical = full_name.split(' ')
        short_name = _technical[0] + ' ' + _technical[1]
        names = [full_name, short_name, father_name]
        print(names)
