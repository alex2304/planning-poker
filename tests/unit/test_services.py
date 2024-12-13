from unittest.mock import MagicMock

import pytest

from exceptions import HttpNotFoundError, HttpBadRequestError
from services import room_service
from services.room_service import init_storage
from storage.base import BaseStorage


@pytest.fixture(scope="module")
def storage_mock():
    mock = MagicMock(spec=BaseStorage)
    init_storage(mock)
    return mock


def test_create_room(storage_mock):
    room_id = room_service.create_room()
    storage_mock.create_room.assert_called_once_with(room_id)


def test_get_room_success(storage_mock):
    storage_mock.get_room.return_value = {"participants": {}, "status": "start"}
    room_id = "room123"
    room = room_service.get_room(room_id)
    storage_mock.get_room.assert_called_once_with(room_id)
    assert room == {"participants": {}, "status": "start"}


def test_get_room_not_found(storage_mock):
    storage_mock.get_room.return_value = None
    room_id = "room123"
    with pytest.raises(HttpNotFoundError):
        room_service.get_room(room_id)


def test_join_room_success(storage_mock):
    storage_mock.get_room.return_value = {"participants": {}, "status": "start"}
    storage_mock.replace_room_participant.return_value = {
        "participants": {"John": -1},
        "status": "start",
    }
    room_id = "room123"
    name = "John"
    room = room_service.join_room(room_id, name)
    storage_mock.replace_room_participant.assert_called_once_with(room_id, name)
    assert room == {"participants": {"John": -1}, "status": "start"}


def test_join_room_not_found(storage_mock):
    storage_mock.get_room.return_value = None
    room_id = "room123"
    name = "John"
    with pytest.raises(HttpNotFoundError):
        room_service.join_room(room_id, name)


def test_join_room_duplicate_participant(storage_mock):
    storage_mock.get_room.return_value = {"participants": {"John": -1}, "status": "start"}
    room_id = "room123"
    name = "John"
    with pytest.raises(HttpBadRequestError):
        room_service.join_room(room_id, name)


def test_leave_room_success(storage_mock):
    storage_mock.get_room.return_value = {"participants": {"John": -1}, "status": "start"}
    storage_mock.remove_room_participant.return_value = {"participants": {}, "status": "start"}
    room_id = "room123"
    name = "John"
    room = room_service.leave_room(room_id, name)
    storage_mock.remove_room_participant.assert_called_once_with(room_id, name)
    assert room == {"participants": {}, "status": "start"}


def test_leave_room_not_found(storage_mock):
    storage_mock.get_room.return_value = None
    room_id = "room123"
    name = "John"
    with pytest.raises(HttpNotFoundError):
        room_service.leave_room(room_id, name)


def test_leave_room_nonexistent_participant(storage_mock):
    storage_mock.get_room.return_value = {"participants": {}, "status": "start"}
    room_id = "room123"
    name = "John"
    with pytest.raises(HttpBadRequestError):
        room_service.leave_room(room_id, name)


def test_start_voting_success(storage_mock):
    storage_mock.get_room.return_value = {"participants": {"John": 0}, "status": "start"}
    storage_mock.set_room_status.return_value = {
        "participants": {"John": -1},
        "status": "voting",
    }
    room_id = "room123"
    room = room_service.start_voting(room_id)
    storage_mock.set_room_status.assert_called_with(room_id, "voting")
    assert room == {"participants": {"John": -1}, "status": "voting"}


def test_start_voting_already_started(storage_mock):
    storage_mock.get_room.return_value = {"participants": {"John": 0}, "status": "voting"}
    room_id = "room123"
    with pytest.raises(HttpBadRequestError):
        room_service.start_voting(room_id)


def test_make_vote_success(storage_mock):
    storage_mock.get_room.return_value = {"participants": {"John": -1}, "status": "voting"}
    storage_mock.set_vote.return_value = {"participants": {"John": 5}, "status": "voting"}
    room_id = "room123"
    name = "John"
    value = 5
    room = room_service.make_vote(room_id, name, value)
    storage_mock.set_vote.assert_called_once_with(room_id, name, value)
    assert room == {"participants": {"John": 5}, "status": "voting"}


def test_end_voting_success(storage_mock):
    storage_mock.get_room.return_value = {"participants": {"John": 5}, "status": "voting"}
    storage_mock.set_room_status.return_value = {
        "participants": {"John": 5},
        "status": "results",
    }
    room_id = "room123"
    room = room_service.end_voting(room_id)
    storage_mock.set_room_status.assert_called_with(room_id, "results")
    assert room == {"participants": {"John": 5}, "status": "results"}


def test_end_voting_not_found(storage_mock):
    storage_mock.get_room.return_value = None
    room_id = "room123"
    with pytest.raises(HttpNotFoundError):
        room_service.end_voting(room_id)
