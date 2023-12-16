import uuid

from flask import Flask,request
from db import stores,items
from flask_smorest import abort



app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        abort(404,message="Bad Request, Ensure 'name' is included in the JSON Payload" )

    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message=f"Store Already exists")

    store_id=uuid.uuid4().hex
    data = {**store_data,"id":store_id}
    stores[store_id]=data
    return data

@app.post("/item")
def create_item():
    item_data = request.get_json()

    if(
        "price" not in item_data or
        "name" not in item_data or
        "store_id" not in item_data
    ):
        print("Validation failed")
        abort(
            400,
            message = "Bad Request, ensure 'Price','Name','store_id' are included in the JSON Payload."
        )
    for item in items.values():
        if (item_data["name"] == item["name"] and item_data["store_id"]==item["store_id"]):
            abort(400,message=f"Item Already exists")

    if item_data["store_id"] not in stores:
        return {"message":"Store Not Found"},404

    item_id = uuid.uuid4().hex
    item = {**item_data,"id":item_id}
    items[item_id] = item

    return item


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,message="Store Not Found")

@app.get("/item")
def get_all_items():
    return {"item":list(items.values())}

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item Deleted"}
    except KeyError:
        abort(404,message="Item Not Found")

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store Deleted"}
    except KeyError:
        abort(404, message="Item Not Found")

@app.put("/item/<string:item_id>")
def update_items(item_id):
    item_data = request.get_json()
    if "price" not in item_data and "name" not in item_data:
        abort(404,message="Ensure 'price' and 'name' are in JSON Payload")
    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404,message="Item Not Found")




