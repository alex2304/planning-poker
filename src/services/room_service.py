import threading
import uuid
from typing import Optional

from exceptions import HttpNotFoundError, HttpBadRequestError
from storage.base import BaseStorage
from utils.util import with_lock

_storage_lock = threading.Lock()

storage: Optional[BaseStorage] = None


def init_storage(_storage: Optional[BaseStorage] = None) -> Optional[BaseStorage]:
    global storage
    if storage is None:
        storage = _storage
    return storage


@with_lock(_storage_lock)
def create_room() -> str:
    room_id = str(uuid.uuid4())[:8]
    storage.create_room(room_id)
    return room_id


@with_lock(_storage_lock)
def get_room(room_id: str) -> dict:
    room = storage.get_room(room_id)
    if room is None:
        raise HttpNotFoundError(f"Room {room_id} not found")
    return room


@with_lock(_storage_lock)
def join_room(room_id: str, name: str) -> dict:
    room = storage.get_room(room_id)
    if room is None:
        raise HttpNotFoundError(f"Room {room_id} not found")
    if name in room["participants"]:
        raise HttpBadRequestError("Participant already in the room")
    updated_room = storage.replace_room_participant(room_id, name)
    return updated_room


@with_lock(_storage_lock)
def leave_room(room_id: str, name: str) -> dict:
    room = storage.get_room(room_id)
    if room is None:
        raise HttpNotFoundError(f"Room {room_id} not found")
    if name not in room["participants"]:
        raise HttpBadRequestError("Participant is not in the room")
    updated_room = storage.remove_room_participant(room_id, name)
    return updated_room


@with_lock(_storage_lock)
def start_voting(room_id: str) -> dict:
    room = storage.get_room(room_id)
    if room is None:
        raise HttpNotFoundError(f"Room {room_id} not found")
    if room["status"] == 'voting':
        raise HttpBadRequestError("Voting already started")
    for name in room["participants"]:
        room["participants"][name] = -1
    updated_room = storage.set_room_status(room_id, "voting")
    return updated_room


@with_lock(_storage_lock)
def make_vote(room_id: str, name: str, value: str) -> dict:
    room = storage.get_room(room_id)
    if room is None:
        raise HttpNotFoundError(f"Room {room_id} not found")
    if name not in room["participants"]:
        raise HttpBadRequestError("Participant is not in the room")
    updated_room = storage.set_vote(room_id, name, value)
    return updated_room


@with_lock(_storage_lock)
def end_voting(room_id: str) -> dict:
    room = storage.get_room(room_id)
    if room is None:
        raise HttpNotFoundError(f"Room {room_id} not found")
    updated_room = storage.set_room_status(room_id, "results")
    return updated_room
