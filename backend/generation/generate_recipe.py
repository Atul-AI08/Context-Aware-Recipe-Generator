import os
import getpass
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableConfig, chain
from langchain_community.tools import TavilySearchResults

from utils import build_dietary_text, get_skill_level_detail
from prompts import recipe_prompt


os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key: ")

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

llm_with_tools = llm.bind_tools([tool])
llm_chain = recipe_prompt | llm_with_tools


@chain
def tool_chain(
    user_input,
    config: RunnableConfig,
) -> str:
    """
    Generates a recipe using tool integration based on the given parameters.

    Args:
        dish_name: Name of the dish.
        dietary_preferences: List of dietary preferences.
        serving: Number of servings.
        config: Optional configuration for the tool.

    Returns:
        A generated recipe string.
    """
    dietary_text = build_dietary_text(user_input["dietary_preferences"])
    detail = get_skill_level_detail(user_input["skill_level"])
    input_ = {
        "dish_name": user_input["dish_name"],
        "dietary_text": dietary_text,
        "skill_level": user_input["skill_level"],
        "detail": detail,
    }

    try:
        ai_msg = llm_chain.invoke(input_, config=config)
        if ai_msg.content:
            return ai_msg.content

        tool_msgs = tool.batch(ai_msg.tool_calls, config=config)
        response = llm_chain.invoke(
            {**input_, "messages": [ai_msg, *tool_msgs]}, config=config
        )

        return response.content if response else "Could not generate recipe."
    except Exception as e:
        print(f"Error generating recipe: {e}")
        return "Could not generate recipe. Please try again."
