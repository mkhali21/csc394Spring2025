from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ---------- SQLite Setup ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./restaurants.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ---------- SQLAlchemy Model ----------
class RestaurantDB(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)

# Create the table
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

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Routes ----------
@app.post("/restaurants/", response_model=Restaurant)
def create_restaurant(restaurant: Restaurant, db: Session = Depends(get_db)):
    db_restaurant = RestaurantDB(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@app.get("/restaurants/", response_model=List[Restaurant])
def list_restaurants(db: Session = Depends(get_db)):
    return db.query(RestaurantDB).all()

@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(RestaurantDB).filter(RestaurantDB.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@app.delete("/restaurants/{restaurant_id}", response_model=Restaurant)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(RestaurantDB).filter(RestaurantDB.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(restaurant)
    db.commit()
    return restaurant
