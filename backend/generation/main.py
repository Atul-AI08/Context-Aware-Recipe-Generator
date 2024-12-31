from generate_recipe import tool_chain
from generate_custom_recipe import generate_custom_recipe
from models import UserInput, CustomInput
from utils import parse_recipe_result

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Context-Aware Recipe Generator",
    version="1.1",
    description="A context-aware recipe generator using LangChain",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.post("/generate-recipe")
async def generate_recipe(input_data: UserInput):
    try:
        result = tool_chain.invoke(input_data.dict())

        ingredients, instructions = parse_recipe_result(result)
        return JSONResponse(
            content={"ingredients": ingredients, "instructions": instructions}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/custom-recipe")
async def custom_recipe(input_data: CustomInput):
    try:
        result = generate_custom_recipe(
            input_data.dish_name,
            input_data.skill_level,
            input_data.recipe,
            input_data.dietary_preferences,
        )

        ingredients, instructions = parse_recipe_result(result)
        return {"ingredients": ingredients, "instructions": instructions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
