"""
Volunteer.su  is a website where a Russian patriotic initiative group
collects and publishes data about military personnel, activists, etc., supporting Ukraine.

Being listed or having a close relative like father listed on this website
is likely to cause problems for an individual at the border.

This module check presence of a person and his father on Volunteer.su and
returns a list with found references or an empty list.

V2 with requests and bs4
No father's name check or ru-ua translation provided
"""
import requests
from bs4 import BeautifulSoup

url = 'https://volunteer.su'

def soup(url: str) -> BeautifulSoup:
    " return soup "
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def adjust(name: str, link: str, content: list, labels: list) -> list:
    """
    return a list of all personal info found
    """
    content = [x for x in content if x != '']
    labels = [x for x in labels if x != '']

    # add a birthday label or one extra label
    if content[0][0].isdigit():
        labels.insert(0, 'ДР:')
    else:
        if len(content) > len(labels):
            labels.insert(0, 'Доп инфо:')

    # in case number of labels still less than number of content fields
    if len(content) > len(labels):
        delta = len(content) - len(labels)
        for _ in range(delta):
            labels.append(f'Доп инфо:')

    assert len(content) == len(labels)
    return [(name,', '.join([f'{l} {c}' for l, c in zip(labels, content)]), link)]

def deep_search(data: list) -> list:
    """
    return all info found on a link page
    """
    for name, link in data:
        relevant_data_raw = soup(link).find_all('div', id='content-wrap')
        field_even = [[i.text for i in x.find_all('div', class_="field-item even")]
                      for x in relevant_data_raw].pop()
        field_label = [[i.text.rstrip('\xa0') for i in x.find_all('div', class_="field-label")]
                       for x in relevant_data_raw].pop()

    return adjust(name, link, field_even, field_label)

def search(fio_raw: str) -> list:
    """
    do a preliminary search
    if anything relevant was found initiate a deeper search
    return a list with info or an empty list
    """
    print(f'Volunteer: checking {fio_raw} on Volunteer.su now')
    fio_split = fio_raw.lower().split(' ')

    # prepare names in the accepted by Volunteer.su format
    # these names are extansion to access a personal links
    fi = f'{fio_split[0]}+{fio_split[1]}'
    fio = f'{fio_split[0]}+{fio_split[1]}+{fio_split[2]}'
    search_names = [fi, fio]

    # to compare findings with names we have
    compare = [f'{fio_split[0]} {fio_split[1]}', fio_raw.lower()]

    relevant_names = []
    for ind in range(len(search_names)):
        name_ext = f'/search?text={search_names[ind]}'
        names_finding = soup(url+name_ext).find_all('h2')
        relevant_names.append([(x.text, url+x.find('a')['href'])
                               for x in names_finding if
                               x.text.lower() == f'{compare[ind]}'])

    # flattening list
    relevant_names = [item for sublist in relevant_names for item in sublist]

    if len(relevant_names) > 0:

        print(f'Volunteer: for name {fio_raw} is found {relevant_names}')
        return deep_search(relevant_names)
    else:
        return []


if __name__ == '__main__':
    # any data provided in Test is random and can not match with any personal information
    TEST = [
        "Шах Виталий Андреевич",
        "Панченко Кирилл Андреевич",
        "Кучма Вадим Васильевич"
    ]
    for data in TEST:
        print(search(data))
        print('*****************************')
