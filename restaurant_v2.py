from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ---------- SQLite Setup ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurants.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ---------- SQLAlchemy Model ----------
class RestaurantDB(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)

## create tables if they don't exist
Base.metadata.create_all(bind=engine)

# ---------- Pydantic Models ----------
class Restaurant(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True

# ---------- FastAPI App ----------
app = FastAPI()

# ---------- Routes ----------
@app.get("/restaurants/", response_model=List[Restaurant])
def read_restaurants():
    with SessionLocal() as session:
        restaurants = session.query(RestaurantDB).all()
        return restaurants

@app.post("/restaurants/", response_model=Restaurant)
def create_restaurant(restaurant: Restaurant):
    with SessionLocal() as session:
        db_restaurant = RestaurantDB(**restaurant.dict())
        session.add(db_restaurant)
        session.commit()
        session.refresh(db_restaurant)
        return db_restaurant

@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int):
    with SessionLocal() as session:
        restaurant = session.query(RestaurantDB).filter(RestaurantDB.id == restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return restaurant


@app.delete("/restaurants", response_model=Restaurant)
def delete_restaurant(restaurant_id: int):
    with SessionLocal() as session:
        restaurant = session.query(RestaurantDB).filter(RestaurantDB.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        session.delete(restaurant)
        session.commit()
        return restaurant
