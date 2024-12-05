
from app.database import get_db
from app.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest 
from app.main import app
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "postgresql://sneha:Sneha123@localhost/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db

    Base.metadata.drop_all(bind=engine)
    db.close()



@pytest.fixture()
def client(test_db):

    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as client:
        yield client