from models.enums import RoomStatus
from utils.capped_dict import CappedDict
from .base import BaseStorage


class InMemoryStorage(BaseStorage):

    def __init__(self, *, rooms_limit: int) -> None:
        self._rooms = CappedDict(capacity=rooms_limit)

    def create_room(self, room_id: str) -> None:
        self._rooms[room_id] = {"participants": {}, "status": "start"}

    def get_room(self, room_id: str) -> dict:
        return self._rooms.get(room_id)

    def replace_room_participant(self, room_id: str, name: str) -> dict:
        room = self.get_room(room_id)
        room["participants"][name] = -1
        return room

    def remove_room_participant(self, room_id: str, name: str) -> dict:
        room = self.get_room(room_id)
        del room["participants"][name]
        return room

    def set_room_status(self, room_id: str, status: RoomStatus) -> dict:
        room = self.get_room(room_id)
        room["status"] = status
        return room

    def set_vote(self, room_id: str, name: str, value: str) -> dict:
        room = self.get_room(room_id)
        room["participants"][name] = value
        return room
