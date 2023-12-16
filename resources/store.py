import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort

import db
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from db import db
from models import StoreModel

blp = Blueprint("stores",__name__,description="Operations on Stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted"},200


    # @blp.response(200,StoreSchema)
    # def get(cls,store_id):
    #     try:
    #         return stores[store_id]
    #     except KeyError:
    #         abort(404, message="Store Not Found")
    #
    # def delete(cls,store_id):
    #     try:
    #         del stores[store_id]
    #         return {"message": "Store Deleted"}
    #     except KeyError:
    #         abort(404, message="Item Not Found")


@blp.route("/store")
class StoresList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500,message="An error occurred creating the store")

        return store

    # @blp.response(200,StoreSchema(many=True))
    # def get(cls):
    #     return stores.values()
    #
    # @blp.arguments(StoreSchema)
    # @blp.response(201,StoreSchema)
    # def post(cls,store_data):
    #     # store_data = request.get_json()
    #     #
    #     # if "name" not in store_data:
    #     #     abort(404, message="Bad Request, Ensure 'name' is included in the JSON Payload")
    #
    #     for store in stores.values():
    #         if store["name"] == store_data["name"]:
    #             abort(400, message=f"Store Already exists")
    #
    #     store_id = uuid.uuid4().hex
    #     data = {**store_data, "id": store_id}
    #     stores[store_id] = data
    #     return data