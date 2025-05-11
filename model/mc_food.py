from pydantic import BaseModel
from typing import Dict

class MCFood(BaseModel):
    """
    Represents the data structure of a Mcdonald Food.
    """

    name: str
    calories: str
    fat: str
    fat_dv: str
    carbohydrates: str
    protein: str

    sodium: str
    sodium_dv: str
    description: str
    image_url: str
    image_description: str
    # main_ingredients: list[str]
    # actual_ingredients : list[str]
    all_ingredients: Dict[str, str] 
    contains: list[str]
    invalid: bool
    url: str
