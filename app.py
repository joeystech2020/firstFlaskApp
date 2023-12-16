import os
import uuid


from flask import Flask,request,jsonify
from flask_smorest import abort
from flask_smorest import Api
from flask_migrate import Migrate
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST


from db import db
import models
##app.py file fully ready & ready to be pushed
def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores Rest API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)
    migrate=Migrate(app,db)
    api=Api(app)

    app.config["JWT_SECRET_KEY"] = "138176784703868631318865906779311980016"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_callback):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
    )


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message":"Signature Verification Failed","error":"invalid_token"}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"message":"Request doesn't contain an access token","error":"Authorization required."}),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"]in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {"description":"The token has been revoked","error":"token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return (
            jsonify(
                {
                    "description":"The token is not fresh",
                    "error":"fresh token required",
                }
            ), 401,
        )

    #with app.app_context():
    #    db.create_all()
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)

    return app

