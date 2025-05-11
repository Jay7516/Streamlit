import os
import json
from collections import OrderedDict
def safe_load_json(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
TEMP_DATA = r"json\test.json\temp_data.json"

def add_to_json():
    # Load both source and destination files
    with open(TEMP_DATA, "r") as f:
        source_data = json.load(f)
    destination_data = safe_load_json("all_data.json")
    everything_data = safe_load_json("everything_data.json")
    # Collect all names in the destination to ensure uniqueness
    existing_names = {item["name"] for item in destination_data}

    # Process each item in source
    for item in source_data:
        new_name = item["name"]
        if item.get("invalid") is False and new_name not in existing_names:
            destination_data.append(item)
            existing_names.add(new_name)
        # Write updated destination
    everything_data.extend(source_data)
    with open("all_data.json", "w") as dst_file:
        json.dump(destination_data, dst_file, indent=4)
    with open("everything_data.json", "w") as dst_file:
        json.dump(everything_data, dst_file, indent=4)
def add_ingredients():
    with open(TEMP_DATA, "r+") as f:
        food_list = json.load(f)  # food_list is a list
        if not food_list:
            return
        food = food_list[0]       # get the first item (dict)
        ingredient_types = list(food["all_ingredients"].keys())
        actual_ingredients = list(food["all_ingredients"].values())
        # ingredient_types = food["main_ingredients"]
        # actual_ingredients = food["actual_ingredients"]
        #combined_ingredients = dict(zip(ingredient_types, actual_ingredients))
            # Create a new OrderedDict to enforce order
        reordered_food = OrderedDict()
        reordered_food["main_ingredients"] = ingredient_types
        reordered_food["actual_ingredients"] = actual_ingredients


        reordered_food = OrderedDict()
        for key, value in food.items():
            if key == "all_ingredients":
                # First insert the two new keys BEFORE 'all_ingredients'
                reordered_food["main_ingredients"] = ingredient_types
                reordered_food["actual_ingredients"] = actual_ingredients
            # Now insert the current key
            reordered_food[key] = value

        # Update and save
        food_list[0] = reordered_food
        f.seek(0)
        json.dump(food_list, f, indent=4)
        f.truncate()
def clear_data():
    with open("all_data.json", "w") as f:
        json.dump([], f)
    with open(TEMP_DATA, "w") as f:
        json.dump([], f)
    with open("everything_data.json", "w") as f:
        json.dump([], f)

def dump_data(content):
    data = json.loads(content)
    print(data)
    with open(TEMP_DATA, "w") as f:
        json.dump(data, f, indent=4)
def save_data(content):
    dump_data(content)
    #add_ingredients()
    add_to_json()
