import random 
from scraper import get_book_data, scrape_books


def test_type_of_return():
    """
    Выполняет проверку функции get_book_data.
    Проверяется тип сгенерированных данных и
    наличие в них обязательных полей.
    """
    book_ref = 'a-light-in-the-attic_1000/index.html'
    book_info = get_book_data(
        'http://books.toscrape.com/catalogue/' + book_ref
    )
    result = type(book_info) == dict and set(book_info.keys()).issuperset(
        [
        'Title', 
        'Price', 
        'Star-rating', 
        'Available quantity', 
        'Description'
    ]
    )
    assert result, "Функция должна выводить словарь с обязательными полями"


def test_list_size():
    """
    Выполняет проверку функции scrape_books.
    Проверяется тип и размер сгенерированных данных.
    """
    
    global res
    res = scrape_books()
    assert type(res) == list, "Функция должна выводить список"
    assert len(res) == 1000, \
        "Список должен содержать данные об одной тысяче книг"


def test_list_contetn():
    """
    Выполняет проверку функции scrape_books.
    Проверяется корректность значений, полученных полей.
    """

    check_lst = [
        ['A Light in the Attic', '£51.77', 'Three', '22', ],
        ['Tipping the Velvet', '£53.74', 'One', '20'],
        ['Soumission', '£50.10', 'One', '20'],
        ['Sharp Objects', '£47.82', 'Four', '20'],
        ['Sapiens: A Brief History of Humankind', '£54.23', 'Five', '20'],
        ['The Requiem Red', '£22.65', 'One', '19'],
        ['The Dirty Little Secrets of Getting Your Dream Job', '£33.34',
        'Four', '19'],
        ['''
        The Coming Woman: A Novel Based on the Life of the Infamous Feminist, 
        Victoria Woodhull
        ''', 
        '£17.93', 'Three', '19'],
        ['''
        The Boys in the Boat: 
        Nine Americans and Their Epic Quest for Gold at 
        the 1936 Berlin Olympics
        ''', 
        '£22.60', 'Four', '19'],
        ['The Black Maria', '£52.15', 'One', 'Available quantity']
    ]
    check_num = random.randint(0, 9)
    check_1 = res[check_num]['Title'] == check_lst[check_num][0]
    check_2 = res[check_num]['Price'] == check_lst[check_num][1]
    check_3 = res[check_num]['Star-rating'] == check_lst[check_num][2]
    check_4 = res[check_num]['Available quantity'] == check_lst[check_num][3]
    result_check = check_1 == check_2 == check_3 == check_4
    assert result_check, "Неверное содержание выводимого списка"