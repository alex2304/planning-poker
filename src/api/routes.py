from flask import jsonify, request

from services import room_service

from . import bp


@bp.route("/room", methods=["POST"])
def create_room():
    room_id = room_service.create_room()
    return jsonify({"room_id": room_id}), 201


@bp.route("/room/<room_id>", methods=["GET"])
def get_room(room_id):
    room = room_service.get_room(room_id)
    return jsonify(room), 200


@bp.route("/room/<room_id>/join", methods=["POST"])
def join_room(room_id):
    name = request.form["name"]
    response = room_service.join_room(room_id, name)
    return jsonify(response), 200


@bp.route("/room/<room_id>/leave", methods=["POST"])
def leave_room(room_id):
    name = request.form["name"]
    response = room_service.leave_room(room_id, name)
    return jsonify(response), 200


@bp.route("/room/<room_id>/vote", methods=["POST"])
def make_vote(room_id):
    name = request.form["name"]
    value = request.form["value"]
    response = room_service.make_vote(room_id, name, value)
    return jsonify(response), 200


@bp.route("/room/<room_id>/start_voting", methods=["POST"])
def start_voting(room_id):
    response = room_service.start_voting(room_id)
    return jsonify(response), 200


@bp.route("/room/<room_id>/end_voting", methods=["POST"])
def end_voting(room_id):
    response = room_service.end_voting(room_id)
    return jsonify(response), 200
