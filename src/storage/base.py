from abc import ABC, abstractmethod
from typing import Dict, Optional

from models.enums import RoomStatus


class BaseStorage(ABC):
    @abstractmethod
    def create_room(self, room_id: str) -> str:
        pass

    @abstractmethod
    def get_room(self, room_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def replace_room_participant(self, room_id: str, name: str) -> Dict:
        pass

    @abstractmethod
    def remove_room_participant(self, room_id: str, name: str) -> Dict:
        pass

    @abstractmethod
    def set_room_status(self, room_id: str, status: RoomStatus) -> Dict:
        pass

    @abstractmethod
    def set_vote(self, room_id: str, name: str, value: str) -> Dict:
        pass
