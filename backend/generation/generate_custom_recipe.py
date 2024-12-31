from typing import List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from utils import ollama_llm


vectorstore = Chroma(
    persist_directory="chroma_store",
    embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    collection_name="test",
)


def get_relevant_context(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join(doc.page_content for doc in docs)


def generate_custom_recipe(
    dish_name: str,
    skill_level: str,
    recipe: str,
    dietary_preferences: Optional[List[str]] = None,
) -> str:
    """
    Modifies an existing recipe based on user specifications.

    Args:
        dish_name: Name of the dish.
        dietary_preferences: List of dietary preferences.
        serving: Number of servings.
        recipe: Original recipe to be modified.
        config: Optional configuration for the tool.

    Returns:
        A modified recipe string.
    """

    context = ""
    if dietary_preferences:
        for preference in dietary_preferences:
            query = (
                f"Substitutions for {dish_name} with dietary preference {preference}"
            )
            context += get_relevant_context(query) + "\n\n"

    question = (
        f"Modify the following recipe to meet the user's preferences.\n\n"
        f"Dish Name: {dish_name}\n\n"
        f"Preferences: {', '.join(dietary_preferences)}\n\n"
        f"Skill Level: {skill_level}\n\n"
        f"Base Recipe:\n\n{recipe}\n\n"
        f"Use these suggestions for substitutions:\n\n{context}\n\n"
        "Please provide a recipe with the ingredients and instructions in the following format:\n\n"
        "Ingredients:\n"
        "quantity1 ingredient_name1\n"
        "quantity2 ingredient_name2\n"
        "...\n\n"
        "Instructions:\n"
        "step1\n"
        "step2\n"
        "...\n\n"
        "STRICTLY FOLLOW THIS FORMAT WITHOUT EXTRA TEXT."
    )

    return ollama_llm(question)
