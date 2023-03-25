from models import Publisher, Book, Stock, Sale, Shop
from podkl import session

def shop_name(publisher_name):
    total = []
    name = []
    finish = []
    shop_id_total = []
    shop_id_total_1 = []
    subq = session.query(Publisher.id).filter(Publisher.name == publisher_name).subquery()
    for c in session.query(Book.id).join(subq, Book.id_publisher == subq.c.id).all():
        total.append(*c)
    total_int = [int(x) for x in total]
    for j in total_int:
        shop_id = session.query(Stock.id_shop).filter(Stock.id_book == j).all()
        shop_id_total.append(shop_id)
    for f in range(len(shop_id_total)):
        for f1 in shop_id_total[f]:
            shop_id_total_1.append(*f1)
    y = (list(set(shop_id_total_1)))
    for b in y:
        shop_name = session.query(Shop.name).filter(Shop.id == b).all()
        name.append(shop_name)
    for s in range(len(name)):
        for p in name[s]:
            finish.append(*p)
    return (finish)

name_bublisher_big = []
name_bublisher = input('Введите название издателя ')
for big in session.query(Publisher.name).all():
    name_bublisher_big.append(*big)
session.close()

while name_bublisher not in  name_bublisher_big:
    name_bublisher = input(f'Введите название издателя, одного из {name_bublisher_big} ')
else:
    print(*shop_name(name_bublisher))


