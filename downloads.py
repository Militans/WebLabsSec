from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mysqlconnector://root:1q2w_1q2w@localhost:3306/catalogue'
db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    short_description = db.Column(db.Text)
    characteristics = db.Column(db.Text)
    detailed_description = db.Column(db.Text)
    category_for_site = db.Column(db.String(255))
    cost = db.Column(db.Integer)

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'


# Создаем таблицу в базе данных, если ее еще нет

def add_product(name, description, short_description, characteristics, detailed_description, image_path):
    with app.app_context():
        # Создаем экземпляр Products
        new_product = Products(
            name=name,
            description=description,
            image_url=image_path,
            short_description=short_description,
            characteristics=characteristics,
            detailed_description=detailed_description
        )

        # Добавляем элемент в базу данных
        db.session.add(new_product)
        db.session.commit()


def update_image_path(product_id, new_image_path):
    with app.app_context():
        # Находим продукт по ID
        product = Products.query.get(product_id)

        # Проверяем, существует ли продукт
        if product:
            # Обновляем только поле image_url
            product.cost = new_image_path

            # Сохраняем изменения
            db.session.commit()
        else:
            print(f"Продукт с ID {product_id} не найден.")


def get_product_ids_by_category(category_for_site):
    with app.app_context():
        # Получаем все айди продуктов с указанным category_for_site
        product_ids = Products.query.filter_by(category_for_site=category_for_site).with_entities(Products.id).all()

        # Преобразуем результат в список
        product_ids = [id[0] for id in product_ids]

        return product_ids



def get_product_ids_by_category2():
    with app.app_context():
        # Получаем все айди продуктов с указанным category_for_site
        product_ids = Products.query.with_entities(Products.id).all()

        # Преобразуем результат в список
        product_ids = [id[0] for id in product_ids]

        return product_ids



category = 'rings'
product_ids = get_product_ids_by_category(category)
product_ids2 = get_product_ids_by_category2()

folder_path = 'static/uploads/' + category
files = os.listdir(folder_path)

ring_names = [
    "Изысканное кольцо с бриллиантом",
    "Золотое обручальное кольцо",
    "Розовое золото с изумрудом",
    "Классическое белое золото",
    "Серебряное кольцо с аметистом",
    "Кольцо с бриллиантовым паве",
    "Эксклюзивное кольцо с сапфиром",
    "Трилогия изумрудных камней",
    "Ретро-стиль с рубином и бриллиантами"
]
cost = [random.randint(20000, 100000) for _ in range(30)]

earring_names = [
    "Элегантные серьги с жемчугом",
    "Золотые кольца с бриллиантами",
    "Серьги-гвоздики из розового золота",
    "Серьги с изумрудами и алмазами",
    "Серебряные серьги с сапфирами",
    "Серьги-пусеты с жемчужиной"
]

pendant_names = [
    "Подвеска с жемчугом",
    "Золотая подвеска с бриллиантом",
    "Подвеска в форме сердца",
    "Сапфировая подвеска на цепочке",
    "Подвеска с рубином и алмазами",
    "Подвеска-крест с изумрудами",
    "Эксклюзивная подвеска с аметистом"
]




necklace_names = [
    "Колье с жемчужинами",
    "Золотое колье с алмазами",
    "Колье из белого золота",
    "Изысканное колье с сапфирами",
    "Колье с рубинами и жемчугом",
    "Элегантное колье с изумрудами",
    "Колье-цепочка с подвеской",
    "Колье в стиле винтаж"
]



rings_d = [
    "Золотое кольцо с бриллиантом, золото 18 карат, 5 грамм, один бриллиант 0.75 карата, классический, жёлтое золото",
    "Золотое кольцо с изумрудом, золото 14 карат, 4.2 грамма, один изумруд 1.2 карата, элегантный, белое золото",
    "Золотое кольцо с сапфиром, золото 22 карата, 6.5 грамма, один сапфир 1.5 карата, ретро, красное золото",
    "Золотое кольцо с жемчугом, золото 20 карат, 5.8 грамма, один жемчуг диаметром 8 мм, винтаж, розовое золото",
    "Золотое кольцо 'Солнце', золото 24 карата, 7.2 грамма, дизайн в виде солнца с тремя лучами, авангардный, жёлтое золото",
    "Золотое кольцо с рубинами, золото 18 карат, 6.9 грамма, два рубина по 1.2 карата каждый, роскошный, белое золото",
    "Золотое кольцо с топазом, золото 14 карат, 4.5 грамма, один синий топаз 0.9 карата, повседневный, жёлтое золото",
    "Золотое кольцо с аквамарином, золото 20 карат, 5.6 грамма, один аквамарин 1.3 карата, морской, розовое золото",
    "Золотое кольцо с аметистом, золото 22 карата, 6.1 грамма, один аметист 1.4 карата, мистический, красное золото"
]


print(len(files))
print(len(product_ids))


for i in range(30):
    update_image_path(product_ids2[i], cost[i])



# Закрываем соединение с базой данных
db.session.remove()
