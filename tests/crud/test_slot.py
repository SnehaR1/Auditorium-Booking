from fastapi.testclient import TestClient

from app.main import app

import pytest

client = TestClient(app)


def test_add_slot(client):
    headers={"X-Custom-Header":"Token123"}
    slot_data={
    "date": "2024-12-07",
    "slot_name": "DDLJ",
    "start_time": "10:00:00",
    "end_time": "12:30:00"
    }
    response=client.post("/slot/1/",json=slot_data,headers=headers)

    assert response.status_code==200
    assert response.json()=={
    "message": "Slot for the Auditorium added!",
    "slot": {
    "date": "2024-12-07",
    "auditorium_id": 1,
    "start_time": "10:00:00",
    "end_time": "12:30:00",
    "slot_name": "DDLJ",
    "id": 1
    }
    }

