import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from utils import load_data_from_json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Services.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JSON_AS_ASCII"] = False

db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    email = Column(String(100))
    phone = Column(String(100))

    orders = relationship("Order")


class Executor(db.Model):
    __tablename__ = "executor"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    email = Column(String(100))
    phone = Column(String(100))

    offers = relationship("Offer")
    orders = relationship("Order")


class Offer(db.Model):
    __tablename__ = "offer"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    executor_id = Column(Integer, ForeignKey("executor.id"))

    orders = relationship("Order")


class Order(db.Model):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(1000))
    start_date = Column(String)
    end_date = Column(String)
    address = Column(String(300))
    price = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    executor_id = Column(Integer, ForeignKey("executor.id"))

    offers = relationship("Offer", overlaps="orders")


db.create_all()

users_list = load_data_from_json("users.json")

# Добавление пользователей в таблицы Исполнитель/Заказчик (проведена нормализация таблицы Users)
# При попытке вывести логику добавления в отдельный модуль Питон ругается на круговую ссылку между модулями

customers_for_add = []
executors_for_add = []

for user in users_list:
    if user['role'] == "executor":
        executor_add = Executor(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            phone=user['phone']
        )
        executors_for_add.append(executor_add)
    else:
        customer_add = Customer(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            phone=user['phone']
        )
        customers_for_add.append(customer_add)

# Добавление данных в таблицу Заказы

orders_list = load_data_from_json("orders.json")
orders_for_add = []

for order in orders_list:
    order_add = Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    )
    orders_for_add.append(order_add)

# Добавление данных в таблицу предложения

offers_list = load_data_from_json("offers.json")
offers_for_add = []

for offer in offers_list:
    offer_add = Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id']
    )
    offers_for_add.append(offer_add)


#db.session.add_all(customers_for_add)
#db.session.add_all(executors_for_add)
#db.session.add_all(orders_for_add)
#db.session.add_all(offers_for_add)

#db.drop_all()
db.session.commit()
