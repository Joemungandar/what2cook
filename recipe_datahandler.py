# Die ersten 10 Rezepte wurden von mir handlich erstellt, alle weiteren habe ich nach dem Vorbild der ersten 10 mir von ChatGPT erstellen lassen

import json, os

JSON_FILE_NAME = "recipes_data.json"
PATH_TO_JSON = os.path.join(os.getcwd(), JSON_FILE_NAME)

def save_to_json(recipe_data=[]):
    print("Save to JSON-File...")
    with open(PATH_TO_JSON,"w",encoding="UTF-8") as recipes_json:
        json.dump(recipe_data, recipes_json, indent=4)
    

def load_from_json() -> dict:
    print("Load from JSON-File...")
    if not os.path.exists(PATH_TO_JSON):
        print("FEHLER: Datei existiert nicht!")
        return []
    with open(PATH_TO_JSON, "r", encoding="UTF-8") as recipes_json:
        recipes_data = json.load(recipes_json)
        return recipes_data

rezept_sammlung = load_from_json()

def get_ingredients(recipe_name) -> list:
    global rezept_sammlung
    try:
        recipe = rezept_sammlung[recipe_name]
        ingredients = recipe.get("Zutaten")
        return ingredients
    except(KeyError):
        print("FEHLER: Rezeptsammlung hat kein Rezept mit dem Namen", recipe_name)
        return []

def get_cooktime(recipe_name) -> list:
    global rezept_sammlung
    recipe = rezept_sammlung[recipe_name]
    cooktime = recipe.get("Kochzeit")
    return cooktime

def get_veggie(recipe_name) -> list:
    global rezept_sammlung
    recipe = rezept_sammlung[recipe_name]
    veggie = recipe.get("vegetarisch")
    return veggie

def get_vegan(recipe_name) -> list:
    global rezept_sammlung
    recipe = rezept_sammlung[recipe_name]
    vegan = recipe.get("vegan")
    return vegan

if __name__ == "__main__":
    data = load_from_json()
    print(data)
    save_to_json(rezept_sammlung)
    data = load_from_json()
    print(data, type(data))
    get_ingredients("Pasta")
    get_ingredients("Lasagne")