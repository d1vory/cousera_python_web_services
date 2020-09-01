from bs4 import BeautifulSoup
import unittest


def imageWidthIsValid(tag):
    return tag.name == 'img' and tag.has_attr('width') and int(tag['width']) >= 200


def headersAreValid(tag):
    validHeaders = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    validLetters = ['E', 'T', 'C']

    if tag.name not in validHeaders:
        return False

    if tag.string:
        return tag.string[0] in validLetters
    else:
        return tag.text[0] in validLetters

def maxLinksLen(body):
    allLinks = body.find_all('a')
    maxCount = 0
    for link in allLinks:
        l = 1
        siblings = link.find_next_siblings()
        for sibling in siblings:
            if sibling.name == 'a':
                l += 1
            else:
                break;

        if l > maxCount:
            maxCount = l
    return maxCount

def unNestedLists(tag):
    return (tag.name == 'ul' or tag.name == 'ol') and (len(tag.find_parents(['ul','ol'])) == 0)



def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError

    with open(path_to_file, encoding='utf-8') as file:

        soup = BeautifulSoup(file, 'html.parser')
        body = soup.find(id='bodyContent')

        images = len(body.find_all(name=imageWidthIsValid))
        headers = len(body.find_all(name=headersAreValid))
        linkslen = maxLinksLen(body)
        lists = len(body.find_all(name= unNestedLists))


    return [images, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
    #parse('wiki/Stone_Age')