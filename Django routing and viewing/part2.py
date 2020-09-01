import os
from bs4 import BeautifulSoup
import re
from .parser import parse

def getLinks(path,file):
    try:
        with open(os.path.join(path, file), encoding="utf-8") as page:
            soup = BeautifulSoup(page, 'lxml')
            links = soup.find_all(
                lambda tag: tag.name == 'a' and tag.has_attr('href') and tag['href'].startswith('/' + path))

            #links2 = re.findall(r"(?<=/wiki/)[\w()]+", page.read())

            res = [ link['href'][6:]   for link in links  ]
            return res
    except (FileNotFoundError,NotADirectoryError):
        return []

def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    if start_page == end_page:
        return [start_page]


    queue= [start_page]
    #can be replaced with dictionary
    visited = {start_page:True}
    predecessors ={start_page:''}

    while queue:
        file = queue.pop(0)

        for page in getLinks(path,file):
            if page not in visited:
                queue.append(page)
                visited[page] = True
                predecessors[page] = file


            if page == end_page:
                #print(visited)
                #print(predecessors[page])
                queue.clear()
                break

    res = []
    current = end_page
    while True:
        res.insert(0,current)
        if current == start_page:
            break
        current = predecessors[current]
    print(res)

    return res



def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь

    return {page: parse(path +  page)   for page in pages }


