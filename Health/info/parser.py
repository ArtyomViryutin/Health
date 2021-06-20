import re
from bs4 import BeautifulSoup
import requests
import urllib3
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


DOCUMENT_URL = 'https://docs.cntd.ru/api/document/436733768'
BLOCK_URL = 'content/text/block'

PREFIXES = {'В': 'B', 'Т': 'T', 'С': 'C', 'Н': 'H', 'Р': 'P',
            'О': 'O', 'А': 'A', 'Е': 'E', 'К': 'K', 'М': 'M'}


def custom_range(start, end, step):
    rng = []
    while start <= end:
        rng.append(start)
        if isinstance(start, float):
            start = (start * 10.0 + step * 10.0) / 10.0
        else:
            start += step
    return rng


def get_code_range(code):
    start, end = [code[1:].strip(' *+') for code in code.split('-')]
    if '.' not in (start + end):
        codes = custom_range(int(start), int(end), 1)
    else:
        codes = custom_range(float(start), float(end), 0.1)
    return [(str(code) if code > 10 else '0' + str(code)) for code in codes]


def process_code(code):
    prefix = code[0]
    if '-' in code:
        codes = get_code_range(code)
    else:
        codes = [code[1:].strip(' *+')]
    if prefix in PREFIXES:
        prefix = PREFIXES.get(prefix)
    return [prefix + cd for cd in codes]


def parse_mkb10():
    names = dict()
    with open('./mkb10.csv', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            names[row[2]] = row[3]
    return names


def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    titles = soup.findAll('h5')
    tables = soup.findAll('table', class_='wideTable')
    names = parse_mkb10()
    result = []
    for i in range(len(titles)):
        data = dict()
        title = titles[i].text
        data['criteria'] = [row.text.strip() for row in tables[i].findAll('td', class_='td5')[1:]]
        groups = re.match(r'\d+\.\d+\.\d+\. (?P<description>.+)\(.*:(?P<codes>.*)\)', title)
        data['description'] = groups.group('description').strip()
        codes = []
        sep = ';' if ';' in groups.group('codes') else ','
        for code in groups.group('codes').split(sep):
            code = code.strip()
            cds = process_code(code)
            codes.append(cds)
        data['codes'] = sum(codes, [])
        for code in data.get('codes'):
            if code in names:
                data['name'] = names.get(code)
                break
        result.append(data)
    return result


def parse_document(document_url=DOCUMENT_URL, block_url=BLOCK_URL):
    index = ''
    block_number = requests.get(document_url, verify=False).json()['data']['content']['text']['blocks']
    for num in range(2, block_number + 1):
        response = requests.get(f'{document_url}/{block_url}/{num}', verify=False)
        index += response.text
    data = parse_page(index)
    return data




