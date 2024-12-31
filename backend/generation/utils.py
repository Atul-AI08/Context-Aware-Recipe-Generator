from typing import List, Optional
import ollama


SKILL_LEVEL_DETAIL = {
    "Beginner": "detailed step-by-step",
    "Intermediate": "standard step-by-step",
    "Advanced": "concise, professional",
}


def parse_recipe_result(result: str):
    """Parse the result into ingredients and instructions."""
    ingredients, instructions = [], []
    if "Instructions:" in result and "Ingredients:" in result:
        ingredients = (
            result.split("Instructions:")[0]
            .split("Ingredients:")[1]
            .strip()
            .split("\n")
        )
        instructions = result.split("Instructions:")[1].strip().split("\n")
    return ingredients, instructions


def build_dietary_text(dietary_preferences: Optional[List[str]]) -> str:
    """Creates dietary preference text for the prompt."""
    return f" that is {', '.join(dietary_preferences)}" if dietary_preferences else ""


def get_skill_level_detail(skill_level: str) -> str:
    """Gets the appropriate instruction detail level based on skill level."""
    return SKILL_LEVEL_DETAIL.get(skill_level, "standard step-by-step")


def ollama_llm(question: str) -> str:
    """Formats prompt and interacts with the LLM."""
    response = ollama.chat(
        model="dolphin-mixtral", messages=[{"role": "user", "content": question}]
    )
    return response["message"]["content"]
