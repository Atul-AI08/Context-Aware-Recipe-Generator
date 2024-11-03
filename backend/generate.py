import getpass
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_community.tools import TavilySearchResults


app = FastAPI(
    title="Context-Aware Recipe Generator",
    version="1.0",
    description="A context-aware recipe generator using LangChain",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
)

os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
)

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful assistant that generates detailed recipes. Please provide a recipe with the ingredients and instructions in the following format:\n\n"
            "Ingredients:\n"
            "quantity1 ingredient_name1\n"
            "quantity2 ingredient_name2\n"
            "...\n\n"
            "Instructions:\n"
            "step1\n"
            "step2\n"
            "...\n\n"
            "AVOID ANY OTHER TEXT IN THE OUTPUT AND MAKE SURE THAT THE OUTPUT IS IN THE FORMAT SHOWN ABOVE.",
        ),
        ("human", "Generate a recipe for {dish_name}{dietary_text}."),
        ("placeholder", "{messages}"),
    ]
)

llm_with_tools = llm.bind_tools([tool])

llm_chain = prompt | llm_with_tools


def tool_chain(
    dish_name: str, dietary_preferences: Optional[List[str]], config: RunnableConfig
):
    if dietary_preferences:
        preferences_str = ", ".join(dietary_preferences)
        dietary_text = f" that is {preferences_str}"
    else:
        dietary_text = ""

    input_ = {
        "dish_name": dish_name,
        "dietary_text": dietary_text,
    }

    ai_msg = llm_chain.invoke(input_, config=config)
    tool_msgs = tool.batch(ai_msg.tool_calls, config=config)
    return llm_chain.invoke({**input_, "messages": [ai_msg, *tool_msgs]}, config=config)


class UserInput(BaseModel):
    dish_name: str
    dietary_preferences: Optional[List[str]] = None  # Vegan, Gluten-free, etc.


@app.post("/generate-recipe")
async def generate_recipe(input_data: UserInput):
    try:
        config = RunnableConfig()

        result = tool_chain(
            input_data.dish_name, input_data.dietary_preferences, config
        )

        ingredients = []
        instructions = []

        ingredients = (
            result.content.split("Instructions:")[0]
            .split("Ingredients:")[1]
            .strip()
            .split("\n")
        )

        instructions = result.content.split("Instructions:")[1].strip().split("\n")

        return {
            "ingredients": ingredients,
            "instructions": instructions,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)
