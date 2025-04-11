from fastapi import FastAPI

app = FastAPI()

restaurant_list = []

@app.get("/restaurants")
async def get_strings():
    return {"restaurants": restaurant_list}

@app.post("/restaurants")
async def add_string(name: str = ""):
    restaurant_list.append(name)
    return {"restaurants": restaurant_list}

@app.delete("/restaurants")
async def delete_string(index: int = 0):
    restaurant_list.pop(index)
    return {"restaurants": restaurant_list}
