import json

import requests
from flask import request

from Model_db import app, Customer, Executor, Offer, Order, db


@app.route("/users", methods=("POST", "GET"))
def handle_users():
    """Вывод всех пользователей и добавление нового"""

    if request.method == 'GET':
        customer_list = Customer.query.all()
        executor_list = Executor.query.all()

        user_response = []

        for customer in customer_list:
            user_response.append(
                {
                    "id": customer.id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "age": customer.age,
                    "email": customer.email,
                    "phone": customer.phone,
                    "role": "customer"
                })
        for executor in executor_list:
            user_response.append(
                {
                    "id": executor.id,
                    "first_name": executor.first_name,
                    "last_name": executor.last_name,
                    "age": executor.age,
                    "email": executor.email,
                    "phone": executor.phone,
                    "role": "executor"
                })

        return json.dumps(user_response)
    elif request.method == 'POST':
        if request.is_json:
            user = request.get_json()
            if user['role'] == "customer":
                new_customer = Customer(
                    id=user['id'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    age=user['age'],
                    email=user['email'],
                    phone=user['phone']
                )
                db.session.add(new_customer)
                db.session.commit()
                return {"Пользователь успешно добавлен"}
            elif user['role'] == "executor":
                new_executor = Executor(
                    id=user['id'],
                    first_name=user['first_name'],
                    last_name=user['last_name'],
                    age=user['age'],
                    email=user['email'],
                    phone=user['phone']
                )
                db.session.add(new_executor)
                db.session.commit()
                return {"Пользователь успешно добавлен"}
        else:
            return {"Request is not json"}


@app.route("/users/<int:sid>", methods=["GET", "PUT", "DELETE"])
def handle_one_user(sid: int):
    """Возвращает 1 пользователя по id"""
    data = request.get_json()
    if request.method == "GET":
        user = Executor.query.get(sid)
        if user:
            return json.dumps({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "phone": user.phone,
                "role": "executor"
            })
        else:
            user = Customer.query.get(sid)
            return ({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "phone": user.phone,
                "role": "customer"
            })

    elif request.method == "PUT":
        user = Customer.query.get(sid)
        if user:

            user.id = data['id']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.age = data['age']
            user.email = data['email']
            user.phone = data['phone']
            user.role = "customer"
            db.session.add(user)
            db.session.commit()

            return f"Customer {sid} updated"

        else:
            user = Executor.query.get(sid)
            user.id = data['id']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.age = data['age']
            user.email = data['email']
            user.phone = data['phone']
            user.role = "executor"
            db.session.add(user)
            db.session.commit()

            return f"Executor {sid} updated"

    elif request.method == "DELETE":

        user = Customer.query.get(sid)
        if user:
            db.session.delete(user)
            db.session.commit()
            return f"Customer {sid} deleted"
        else:
            user = Executor.query.get(sid)
            db.session.delete(user)
            db.session.commit()
            return f"Executor {sid} deleted"

@app.route("/offers", methods=['POST', 'GET'])
def handle_offers():
    """Возвращает все предложения и добавляет новое"""
    if request.method == 'GET':
        offer_list = Offer.query.all()
        offer_response = []
        for offer in offer_list:
            offer_response.append({
                "id": offer.id,
                "order_id": offer.order_id,
                "executor_id": offer.executor_id
            })
        return json.dumps(offer_response)
    elif request.method == 'POST':
        if request.is_json:
            offer = request.get_json()
            new_offer = Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            )
            db.session.add(new_offer)
            db.session.commit()
            return "Предложение успешно добавлено"
        else:
            return {"Error! Request is not json"}


@app.route("/offers/<int:sid>", methods=['GET', 'PUT', 'DELETE'])
def handle_one_offer(sid: int):
    """Возвращает, обновляет или удаляет 1 предложение по id"""
    offer = Offer.query.get(sid)

    if request.method == "GET":

        if offer is None:
            return "Offer not found"

        return json.dumps({
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id
        })

    elif request.method == "PUT":
        data = request.get_json()
        offer.id = data['id']
        offer.order_id = data['order_id']
        offer.executor_id = data['executor_id']
        db.session.add(offer)
        db.session.commit()
        return f"Offer {sid} updated"

    elif request.method == "DELETE":
        db.session.delete(offer)
        db.session.commit()
        return f"Offer {sid} deleted"


@app.route("/orders", methods=["POST", "GET"])
def handle_orders():
    """Возвращает все заказы и добавляет новый"""
    if request.method == 'GET':
        order_list = Order.query.all()
        order_response = []
        for order in order_list:
            order_response.append({
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id
            })
        return json.dumps(order_response)
    elif request.method == 'POST':
        if request.is_json:
            order = request.get_json()
            new_order = Order(
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
            db.session.add(new_order)
            db.session.commit()
            return "Заказ успешно добавлен"
        else:
            return {"Error! Request is not json"}


@app.route("/orders/<int:sid>", methods=["GET", "PUT", "DELETE"])
def handle_one_order(sid: int):
    """Возвращает, обновляет, удаляет заказ по id"""

    order = Order.query.get(sid)

    if request.method == "GET":

        if order is None:
            return "Order not found"

        return json.dumps({
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id
        })
    elif request.method == "PUT":
        data = request.get_json()
        order.id = data['id']
        order.name = data['name']
        order.descriptio = data['description']
        order.start_date = data['start_date']
        order.end_date = data['end_date']
        order.address = data['address']
        order.price = data['price']
        order.customer_id = data['customer_id']
        order.executor_id = data['executor_id']

        db.session.add(order)
        db.session.commit()
        return f"Order {sid} updated"

    elif request.method == "DELETE":
        db.session.delete(order)
        db.session.commit()
        return f"Order {sid} deleted"

app.run()
