from fastapi import FastAPI

app = FastAPI()

restaurant_list = ["Chipotle"]


@app.get("/restaurant")
async def root():
     return {"restaurants": restaurant_list}