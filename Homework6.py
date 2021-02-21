import re
from flask import abort
from flask import Flask, request
from sqlalchemy.orm.exc import NoResultFound
from DriverDBStorage import *
from ClientDBStorage import *
from OrderDBStorage import *
from OrderStatus import *

app = Flask(__name__)

DriverDBStorage().insert_test_data()
ClientDBStorage().insert_test_data()


@app.route('/api/v1/drivers')
def show_driver():
    db = DriverDBStorage()
    try:
        driver_id = request.args.get('driverId')
        if int(driver_id) < 0:
            abort(400, "Id не может быть меньше 0")
        return db.get_driver(driver_id).to_json()
    except NoResultFound:
        abort(404, "Driver not found")
    except ValueError:
        abort(400, "Передано неправильное значение id")


@app.route('/api/v1/drivers', methods=["POST"])
def post_driver():
    db = DriverDBStorage()
    if request.method == "POST":
        d_name = request.json['name']
        d_car = request.json['car']
        name_valid = re.match("^[а-яА-яеЁ]{1,20}$", d_name)
        car_valid = re.match("^[a-zA-Z0-9\\s]{1,30}$", d_car)
        if name_valid is not None and car_valid is not None:
            created_row_data = Driver(name=str(d_name),
                                      car=str(d_car))
            db.add_driver(created_row_data)
            return db.get_driver(created_row_data.id).to_json()
        else:
            abort(400, "Bad request")


@app.route('/api/v1/drivers/<int:driver_id>', methods=["DELETE"])
def delete_driver(driver_id):
    db = DriverDBStorage()
    try:
        if int(driver_id) <= 0:
            abort(400, "Id не может быть равен 0")
        driver = db.remove_driver(driver_id)
        return driver.to_json()
    except NoResultFound:
        abort(404, "Driver not found into base")


@app.route('/api/v1/clients')
def show_client():
    db = ClientDBStorage()
    try:
        client_id = request.args.get('clientId')
        if int(client_id) < 0:
            abort(400, "Id не может быть меньше 0")
        return db.get_client(client_id).to_json()
    except NoResultFound:
        abort(404, "Client not found")
    except ValueError:
        abort(400, "Передано неправильное значение id")


@app.route('/api/v1/clients', methods=["POST"])
def post_client():
    db = ClientDBStorage()
    if request.method == "POST":
        c_name = request.json['name']
        is_vip = request.json['is_vip']
        name_valid = re.match("^[а-яА-яеЁ]{1,20}$", c_name)
        is_vip_valid = re.match("[0|1]", is_vip)
        if name_valid is not None and is_vip_valid is not None:
            created_row_data = Client(name=str(c_name),
                                      is_vip=str(is_vip))
            db.add_client(created_row_data)
            return db.get_client(created_row_data.id).to_json()
        else:
            abort(400, "Bad request")


@app.route('/api/v1/clients/<int:client_id>', methods=["DELETE"])
def delete_client(client_id):
    db = ClientDBStorage()
    try:
        if int(client_id) <= 0:
            abort(400, "Id не может быть равен 0")
        client = db.remove_client(client_id)
        return client.to_json()
    except NoResultFound:
        abort(404, "Client not found into base")


@app.route('/api/v1/orders')
def show_order():
    db = OrderDBStorage()
    try:
        order_id = request.args.get('orderId')
        if int(order_id) < 0:
            abort(400, "Id не может быть меньше 0")
        return db.get_order(order_id).to_json()
    except NoResultFound:
        abort(404, "Order not found")
    except ValueError:
        abort(400, "Передано неправильное значение id")


@app.route('/api/v1/orders', methods=["POST"])
def post_order():
    db = OrderDBStorage()
    if request.method == "POST":
        o_address_from = request.json['address_from']
        o_address_to = request.json['address_to']
        o_client_id = request.json['client_id']
        o_driver_id = request.json['driver_id']
        o_date_created = request.json['date_created']
        o_status = request.json['status']
        address_from = re.match("^[.а-яА-яеЁ0-9\s]{1,200}$", o_address_from)
        address_to = re.match("^[.а-яА-яеЁ0-9\s]{1,200}$", o_address_to)
        client_id = re.match("^[0-9]{1,10}$", o_client_id)
        driver_id = re.match("^[0-9]{1,10}$", o_driver_id)
        date_created = re.match(""
                "(19|20)\d\d-((0[1-9]|1[012])-(0[1-9]|[12]\d)|(0[13-9]|1[012])-30|(0[13578]|1[02])-31)"
                , o_date_created)
        status = re.match("^[_a-zA-Z0-9\\s]{1,30}$", o_status)
        if address_from is not None and address_to is not None and client_id is not None and \
                driver_id is not None and date_created is not None and status is not None:
            created_row_data = Order(address_from=str(o_address_from),
                                     address_to=str(o_address_to),
                                     client_id=str(o_client_id),
                                     driver_id=str(o_driver_id),
                                     date_created=str(o_date_created),
                                     status=str(o_status)
                                     )
            db.add_order(created_row_data)
            return db.get_order(created_row_data.id).to_json()
        else:
            abort(400, "Bad request")


@app.route('/api/v1/orders/<int:order_id>', methods=["PUT"])
def update_order(order_id):
    db = OrderDBStorage()
    try:
        if int(order_id) <= 0:
            abort(400, "Id не может быть равен 0")
        order = db.get_order(order_id)
        o_address_from = request.json['address_from']
        o_address_to = request.json['address_to']
        o_client_id = request.json['client_id']
        o_driver_id = request.json['driver_id']
        o_date_created = request.json['date_created']
        o_status = request.json['status']
        address_from = re.match("^[.а-яА-яеЁ0-9\s]{1,200}$", o_address_from)
        address_to = re.match("^[.а-яА-яеЁ0-9\s]{1,200}$", o_address_to)
        client_id = re.match("^[0-9]{1,10}$", o_client_id)
        driver_id = re.match("^[0-9]{1,10}$", o_driver_id)
        date_created = re.match(""
                "(19|20)\d\d-((0[1-9]|1[012])-(0[1-9]|[12]\d)|(0[13-9]|1[012])-30|(0[13578]|1[02])-31)"
                , o_date_created)
        status = re.match("^[_a-zA-Z0-9\\s]{1,30}$", o_status)
        if address_from is not None and address_to is not None and client_id is not None and \
                driver_id is not None and date_created is not None and status is not None:
            order.set_address_from(o_address_from)
            order.set_address_to(o_address_to)
            order.set_client_id(o_client_id)
            order.set_driver_id(o_driver_id)
            order.set_date_created(o_date_created)
            order.set_status(o_status)
            db.update_order(order)
            return db.get_order(order.id).to_json()
    except NoResultFound:
        abort(404, "Order not found into base")
    except OrderStatusInvalidStateException as e:
        abort(400, e)


app.run(host="0.0.0.0", port=5050)
