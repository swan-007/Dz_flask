from typing import Type

import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView

from models import Advertisement, Session
from schema import CreateAdvertisement, UpdateAdvertisement

app = Flask(__name__)


class HttpError(Exception):
    def __init__(self, status_cod: int, msg: str | dict | list):
        self.status_cod = status_cod
        self.msg = msg


@app.errorhandler(HttpError)
def error_h(e: HttpError):
    response = jsonify({"status": "error", "msg": e.msg})
    response.status_code = e.status_cod
    return response


def validate(x: Type[CreateAdvertisement] | Type[UpdateAdvertisement], json_data):
    try:
        py_obj = x(**json_data)
        return py_obj.dict(exclude_none=True)
    except pydantic.ValidationError as e:
        raise HttpError(400, e.errors())


def get_advertisement(s: Session, post_id):
    post_ = s.get(Advertisement, post_id)
    if post_ is None:
        raise HttpError(404, "Такой записи нет")
    return post_


class ApiV1(MethodView):
    def get(self, post_id):
        with Session() as s:
            post_ = get_advertisement(s, post_id)
            return jsonify(
                {
                    "id": post_.id,
                    "heading": post_.heading,
                    "description": post_.description,
                    "date_of_creation": post_.date_of_creation,
                    "User_name": post_.user.name,
                    "id_user": post_.user.id,
                }
            )

    def post(self):
        validate_data = validate(CreateAdvertisement, request.json)
        with Session() as sess:
            new_advertisement = Advertisement(**validate_data)
            sess.add(new_advertisement)
            sess.commit()
            return jsonify({"id": new_advertisement.id})

    def patch(self, post_id):
        validate_data = validate(UpdateAdvertisement, request.json)
        with Session() as s:
            post_ = get_advertisement(s, post_id)
            for key, val in validate_data.items():
                setattr(post_, key, val)
            s.add(post_)
            s.commit()
            return jsonify({"heading": post_.heading})

    def delete(self, post_id):
        with Session() as s:
            post_ = get_advertisement(s, post_id)
            s.delete(post_)
            s.commit()
            return jsonify({"status": "200"})


api_view = ApiV1.as_view("api_v1")

app.add_url_rule(
    "/api/<int:post_id>", view_func=api_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/api", view_func=api_view, methods=["POST"])

if __name__ == "__main__":
    app.run()
