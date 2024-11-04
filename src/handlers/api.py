import uuid

from flask import Blueprint, jsonify, request
from utils.storage import rooms

bp = Blueprint("api", __name__)


@bp.route("/room", methods=["POST"])
def create_room():
    room_id = str(uuid.uuid4())
    rooms[room_id] = {"participants": {}, "status": "start"}
    return jsonify({"room_id": room_id})


@bp.route("/room/<room_id>/join", methods=["POST"])
def join_room(room_id):
    room = rooms.get(room_id)
    if room:
        name = request.form["name"]
        rooms[room_id]["participants"][name] = -1
        return jsonify(room)
    return jsonify({"error": "Room not found"}), 404


@bp.route("/room/<room_id>", methods=["GET"])
def get_room(room_id):
    room = rooms.get(room_id)
    if room:
        return jsonify(rooms[room_id])
    return jsonify({"error": "Room not found"}), 404


@bp.route("/room/<room_id>/start_voting", methods=["POST"])
def start_voting(room_id):
    room = rooms.get(room_id)
    if room:
        for name in room["participants"]:
            room["participants"][name] = -1
        room["status"] = "voting"
        return jsonify(room)
    return jsonify({"error": "Room not found"}), 404


@bp.route("/room/<room_id>/vote", methods=["POST"])
def make_vote(room_id):
    name = request.form["name"]
    value = request.form["value"]
    if room_id in rooms and name in rooms[room_id]["participants"]:
        rooms[room_id]["participants"][name] = value
        return jsonify(rooms[room_id])
    return jsonify({"error": "Participant not found"}), 500


@bp.route("/room/<room_id>/end_voting", methods=["POST"])
def end_voting(room_id):
    if room_id in rooms:
        room = rooms.get(room_id)
        if room:
            room["status"] = "results"
            return jsonify(room)
    return jsonify({"error": "Room not found"}), 404
