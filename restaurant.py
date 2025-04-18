from fastapi import FastAPI, HTTPException
import openai
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

api_key="PUT-YOUR-OPENAI-KEY-HERE"
app = FastAPI()


restaurant_list = ["Chipotle", "Portillos", "Nobu"]
reviews = {
    1: ["Delicious Italian pasta!", "Cozy vibe with classic Italian dishes."],
    2: ["Spicy and bold Mexican tacos.", "Fast service, authentic Mexican flavors."],
    3: ["Light and fresh Japanese sushi.", "Great spot for casual Japanese dining."],
    4: ["I hate italian food in general", "I hated italian food at geordanos"]
}

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

@app.get("/reviews")
async def get_strings(index: int = 0):
    if index <= 0 :
        all_reviews = []
        for review_list in reviews.values():
            all_reviews.extend(review_list)
        return {"reviews": all_reviews}
    elif index <= len(reviews):
        return {"reviews": reviews[index]}
    else :
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/suggestions")
async def get_strings(index: int = 0):
    if index <= 0 or index > len(reviews) :
        raise HTTPException(status_code=404, detail="User not found")
    else :
        try:
            prompt = build_prompt(index)
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return {"suggestion": response.choices[0].message.content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


def build_prompt(user_id):
    user_reviews = reviews[user_id]
    user_reviews_joined = " ".join(user_reviews)
    return """Give suggestions for chicago
        restaurant given these reviews from a user.
        Give me only the name and address of a single restaurant
        """ + user_reviews_joined