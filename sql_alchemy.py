from models import Publisher, Book, Stock, Sale, Shop
from podkl import session

def get_shops(publisher):
    if publisher.isdigit():           #Проверяем состоит ли строка только из чисел
        sub = session.query(Shop.name).\
            join(Stock).\
            join(Book).\
            join(Publisher).\
            filter(Publisher.id == int(publisher)).all()  #Объединяем магазины с стоками, книгами и булицистами и получем магазины где идентификационный номер публициста равен необходимому значению, и сохраняем результат в переменную
    else:
        sub = session.query(Shop.name). \
            join(Stock). \
            join(Book). \
            join(Publisher). \
            filter(Publisher.name == publisher).all() #Объединяем магазины с стоками, книгами и булицистами и получем магазины где имя публициста равен необходимому значению, и сохраняем результат в переменную
    total = [] #Создаем пустой список
    for s in sub: #Проходим в цикле по данным, вернувшимся в запросе
        total.append(s) #Добавляем в список имя магазина
    return (list(set(total)))  #Возвращаем получившийся список


if __name__ == '__main__':
    publisher = input("ввести или имя публициста, или айди: ") #Просим клиента ввести или имя публициста, или айди
    print((get_shops(publisher))) #Передаем полученные данные в функцию

