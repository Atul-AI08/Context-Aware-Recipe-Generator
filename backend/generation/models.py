from pydantic import BaseModel
from typing import List, Optional


class UserInput(BaseModel):
    dish_name: str
    dietary_preferences: Optional[List[str]] = None  # Vegan, Gluten-free, etc.
    skill_level: str  # Beginner, Intermediate, Advanced


class CustomInput(BaseModel):
    dish_name: str
    dietary_preferences: Optional[List[str]] = None  # Vegan, Gluten-free, etc.
    skill_level: str  # Beginner, Intermediate, Advanced
    recipe: str
