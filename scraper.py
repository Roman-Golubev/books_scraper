import re
import requests
from bs4 import BeautifulSoup


def get_book_data(book_url: str) -> dict:
    """
    Возвращает словарь с данными об одной книге.
    
    Args:
        book_url (str): url-адрес страницы с книгой.

    Returns:
        product_info (dict): словарь с данными о книге.
    """

    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")
    product_info = {}
    if soup.find("h1"):
        product_info['Title'] = soup.find("h1").get_text()
    else:
        product_info['Title'] = 'The title is absent'
    if soup.find("p", attrs={"class": "price_color"}):
        product_info['Price'] = soup.find(
            "p",
            attrs={"class": "price_color"}
        ).get_text()[1:]
    else:
        product_info['Price'] = 'The price is absent'    
    if soup.find("p", class_=re.compile(r"star-rating\s\w+")):
        product_info['Star-rating'] = soup.find(
            "p",
            class_=re.compile(r"star-rating\s\w+")
        )['class'][1]
    else:
        product_info['Star-rating'] = 'The star-rating is not given'
    if  soup.find("p", attrs={"class": "instock availability"}):
        product_info['Available quantity'] = re.search(
            r"\((\d{0,1000}) available\)",
            soup.find("p", attrs={"class": "instock availability"}).get_text()
        ).group(1)
    else:
        product_info['Available quantity'] = \
            'The available quantity is not given' 
    if soup.find("div", attrs={"id": "product_description"}):
        product_info['Description'] = soup.find(
            "div", 
            attrs={"id": "product_description"}
        ).find_next_sibling().get_text()
    else:
        product_info['Description'] = 'Description is absent'
    table_info = soup.find("table", attrs={"class": "table table-striped"})
    if table_info:
        for i, row in enumerate(table_info.find_all("tr")):
            if i in [2, 3, 4]:
                product_info[row.find("th").get_text()] = \
                    row.find("td").get_text()[1:]
            else:
                product_info[row.find("th").get_text()] = \
                    row.find("td").get_text()
    return product_info


def scrape_books(is_save: bool = False) -> list:
    """
    Возвращает список словарей с данными о книгах.
    Сохраняет список словарей в файл.
    
    Args:
        is_save (bool): аргумент-флаг - сохранение в файл.

    Returns:
        books_data (list): список словарей с данными о книгах.
    """

    base_url = "https://books.toscrape.com/catalogue/page-1.html"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    pages_count = int(re.search(
        r"Page\s1\sof\s(\d{2,4})",
        soup.find("li", attrs={"class": "current"}).get_text()
    ).group(1))
    books_data = []
    for i in range(1, pages_count+1):
        current_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, "html.parser")
        books_lst = soup.find("ol", attrs={"class": "row"}).find_all("li")
        books_ref_lst = [book.find("a")["href"] for book in books_lst]
        for ref in books_ref_lst:
            book_url = 'https://books.toscrape.com/catalogue/' + ref
            books_data.append(get_book_data(book_url))
    if is_save:
        with open('../artifacts/books_data.txt', 'w', encoding='utf-8') as f:
            for book in books_data:
                f.write(str(book) + '\n')
    return books_data