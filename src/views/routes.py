from flask import redirect, render_template, url_for

from exceptions import HttpNotFoundError
from services import room_service
from . import bp


@bp.route("/")
def index():
    return render_template("index.html", header_text="Planning Poker")


@bp.route("/<room_id>")
def room(room_id):
    try:
        room_service.get_room(room_id)
    except HttpNotFoundError:
        return redirect(url_for("views.index"))

    return render_template("room.html", header_text=f"Planning Poker Game")
