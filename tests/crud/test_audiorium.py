from fastapi.testclient import TestClient

from app.main import app

import pytest

client = TestClient(app)



def test_auditorium_listing(client):
    headers={"X-Custom-Header":"Token123"}
    response = client.get("/auditorium/",headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_add_auditorium(client):
    headers={"X-Custom-Header":"Token123"}
    auditorium_data={
    "name": "Kairali",
    "seating": 150,
    "booking_charge": 160
    }
    response=client.post("/auditorium/",json=auditorium_data,headers=headers)
    assert response.status_code == 200
    assert response.json()=={
    "Message": "Auditorium added Successfully!",
    "auditorium": {
        "name": "Kairali",
        "seating": 150,
        "id": 1,
        "booking_charge": 160
    }
    }

def test_update_auditorium(client):
    headers={"X-Custom-Header":"Token123"}
    auditorium_data={
    "name": "Kairali",
    "seating": 150,
    "booking_charge": 180
    }
    response=client.put("/auditorium/1/",json=auditorium_data,headers=headers)
    assert response.status_code == 200
    assert response.json()=={
    "message": "Auditorium updated!",
    "updated_auditorium": {
    "name": "Kairali",
    "seating": 150,
    "booking_charge": 180,
    "id": 1

    }}

def test_delete_auditorium(client):
    headers={"X-Custom-Header":"Token123"}
    response=client.delete("/auditorium/1/",headers=headers)
    assert response.status_code==200
    assert response.json()=={
    "message": "Auditorium information deleted successfully!"
}



  

