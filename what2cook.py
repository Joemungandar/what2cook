from tkinter import *
import tkinter.messagebox
import recipe_datahandler as rdh

# Grundaufbau:
what_2_cook = Tk()
what_2_cook.title = "What2Cook"
what_2_cook.geometry = "800x800"
cook_frame = Frame(bg="green",relief=RAISED,bd=4)
veggie = BooleanVar()
vegan = BooleanVar()
recipe_data = rdh.rezept_sammlung

# Labels, Textfelder:
label_title = Label(cook_frame, bg="green", fg="black", text="WHAT 2 COOK", font=25, height=3)
label_ingredient_1 = Label(cook_frame, bg="green", fg="black", text="Zutat 1:", height=2)
label_ingredient_2 = Label(cook_frame, bg="green", fg="black", text="Zutat 2:", height=2)
label_ingredient_3 = Label(cook_frame, bg="green", fg="black", text="Zutat 3:", height=2)
label_seperator = Label(cook_frame, bg="green", fg="black", text="-----------------------------------", height=2)
label_cooktime = Label(cook_frame, bg="green", fg="black", text="Kochzeit:", height=2)
label_cooktime_minuten = Label(cook_frame, bg="green", fg="black", text="min", height=2)
label_recipe_title = Label(cook_frame, bg="green", fg="black", text="Mögliche Rezepte", height=2)
label_recipes = Label(cook_frame, bg="white", fg="black", text="REZEPTE", justify=LEFT)
label_recipe_info = Label(cook_frame, bg="green", fg = "black", text="Rezept:", height=2)
label_recipe_details_title = Label(cook_frame, bg="green", fg="black", text="Rezeptdetails", height=2)
label_recipe_details = Label(cook_frame, bg="white", fg="black", text="REZEPTDETAILS", justify=LEFT)
text_ingredient_1 = Entry(cook_frame,bg="lime",fg="black")
text_ingredient_2 = Entry(cook_frame,bg="lime",fg="black")
text_ingredient_3 = Entry(cook_frame,bg="lime",fg="black")
text_cooktime = Entry(cook_frame,bg="lime",fg="black")
text_recipe_info = Entry(cook_frame,bg="orange",fg="black")

### Helper-Methoden:
# Methode holt sich aus der recipes_data.json-Datei die Rezepte heraus,
# in denen "ingredient" vorkommt, fügt sie einer Liste hinzu und gibt diese zurück
def returnRecipesWithIngredient(ingredient):
    global recipe_data
    recipes_with_ingredient = []
    for recipe in recipe_data.keys():
        tmp_ingredients = rdh.get_ingredients(recipe)
        if ingredient in tmp_ingredients:
            recipes_with_ingredient.append(recipe)
    return recipes_with_ingredient

def returnRecipesWithCookingtime(time):
    global recipe_data
    recipes_with_cooktime = []
    for recipe in recipe_data.keys():
        tmp_cooktime = rdh.get_cooktime(recipe)
        # print(tmp_cooktime, type(tmp_cooktime))
        if tmp_cooktime <= time:
            recipes_with_cooktime.append(recipe)
    print(recipes_with_cooktime)
    return recipes_with_cooktime

# Gibt aus der Datenbank alle VEGETARISCHEN Rezepte zurück
def returnRecipesVeggie():
    global recipe_data
    recipes_veggie = []
    for recipe in recipe_data.keys():
        tmp_veggie = rdh.get_veggie(recipe)
        if tmp_veggie:
            recipes_veggie.append(recipe)
    return recipes_veggie

# Gibt aus der Datenbank alle VEGANEN Rezepte zurück
def returnRecipesVegan():
    global recipe_data
    recipes_vegan = []
    for recipe in recipe_data.keys():
        tmp_vegan = rdh.get_vegan(recipe)
        if tmp_vegan:
            recipes_vegan.append(recipe)
    return recipes_vegan

# Für das richtige Handling der Intersection darf keine der Listen leer sein!
def adjustEmptyLists(checkedList, alternative1, alternative2):
    if(len(checkedList) == 0):
        if(len(alternative1) != 0):
            checkedList = alternative1
        if(len(alternative2) != 0):
            checkedList = alternative2
    return checkedList

def getIntersection(list1, list2, list3):
    intersection = set(list1).intersection(list2, list3)
    return intersection

### GUI-Methoden:
# Methode zum Leeren aller Textfelder & Anzeigen
def eraseFields():
    meldung = tkinter.messagebox.askyesno(title="Eingabe leeren",message="Bist Du sicher?")
    if meldung:
        text_ingredient_1.delete(0,END)
        text_ingredient_2.delete(0,END)
        text_ingredient_3.delete(0,END)
        text_cooktime.delete(0,END)
        text_recipe_info.delete(0, END)
        label_recipes["text"] = "ANZEIGE GELÖSCHT"
        label_recipe_details["text"] = "ANZEIGE GELÖSCHT"

# Methode, um ein Textfeld in einen int zu verwandeln bzw. zu überprüfen, ob das Feld leer ist
def convertEntryToInt(entry):
    try:
        tmp_time = entry.get()
        tmp_time = int(tmp_time)
        print(tmp_time, type(tmp_time))
        return tmp_time
    except ValueError:
        print("KOCHZEIT: Kein Eintrag")
        return -1

# Methode zum Ausgeben aller Infos über das Rezept
def recipeInfo():
    searched_recipe = text_recipe_info.get()
    global recipe_data
    info = recipe_data.get(searched_recipe)
    if info == None:
        label_recipe_details["text"] = "Rezept wurde nicht\nin Datenbank gefunden!"
        return
    info_as_string = "REZEPT: " + searched_recipe
    info_as_string += "\n\n Zutaten:"
    for zutat in (info.get("Zutaten")):
        info_as_string += "\n-" + zutat
    info_as_string += "\n\nKochzeit: " + str(info.get("Kochzeit")) + " min"
    if (info.get("vegetarisch")):
        info_as_string += "\n*VEGETARISCH"
    if (info.get("vegan")):
        info_as_string += ", VEGAN"
    label_recipe_details["text"] = info_as_string

def showRecipes():
    cooktime = convertEntryToInt(text_cooktime)
    # 1.) Zutaten aus Feldern auslesen:
    ingredient1 = text_ingredient_1.get()
    ingredient2 = text_ingredient_2.get()
    ingredient3 = text_ingredient_3.get()
    ingredients_empty = len(ingredient1) == len(ingredient2) == len(ingredient3) == 0
    recipes_string = ""
    # print(veggie.get())
    # print(vegan.get())
    # 2.) Rezeptlisten aus jeweils einzelnen Zutaten generieren:
    recipeList_ingredient1 = returnRecipesWithIngredient(ingredient1)
    recipeList_ingredient2 = returnRecipesWithIngredient(ingredient2)
    recipeList_ingredient3 = returnRecipesWithIngredient(ingredient3)
    # print("Rezept-Suche-1:",recipeList_ingredient1)
    # print("Rezept-Suche-2:",recipeList_ingredient2)
    # print("Rezept-Suche-3:",recipeList_ingredient3)
    # 3.) Leere Listen (sofern nicht ALLE leer sind) mit anderen bereits vorhandenen füllen
    recipeList_ingredient1 = adjustEmptyLists(recipeList_ingredient1, recipeList_ingredient2, recipeList_ingredient3)
    recipeList_ingredient2 = adjustEmptyLists(recipeList_ingredient2, recipeList_ingredient1, recipeList_ingredient3)
    recipeList_ingredient3 = adjustEmptyLists(recipeList_ingredient3, recipeList_ingredient2, recipeList_ingredient1)
    # 4.) Schnittmenge aller 3 Listen bestimmen
    recipes_output = getIntersection(recipeList_ingredient1, recipeList_ingredient2, recipeList_ingredient3)
    # 5.) Kochzeit berücksichtigen
    if cooktime != -1:
        recipeList_cooktime = returnRecipesWithCookingtime(cooktime)
        # RANDFALL: Falls NUR Kochzeit eingegeben wurde und keine Zutat
        if(ingredients_empty):
            recipes_output = set(recipeList_cooktime)
        else:
            recipes_output = recipes_output.intersection(recipeList_cooktime)
    # 6.) Vegan berücksichtigen
    if (vegan.get()):
        print("vegan-Branch")
        recipeList_vegan = returnRecipesVegan()
        # RANDFALL: Falls keine Kochzeit UND keine Zutaten eingegeben wurde
        if (cooktime == -1) and ingredients_empty:
            recipes_output = set(recipeList_vegan)
        recipes_output = recipes_output.intersection(recipeList_vegan)
    # 7.) Falls NICHT vegan: Vegetarisch berücksichtigen
    elif (veggie.get()):
        print("Veggie-Branch")
        recipeList_veggie = returnRecipesVeggie()
        # RANDFALL: Falls keine Kochzeit UND keine Zutaten eingegeben wurde
        if (cooktime == -1) and ingredients_empty:
            recipes_output = set(recipeList_veggie)
        recipes_output = recipes_output.intersection(recipeList_veggie)
    # print("Gesamt-Rezeptsuche: ",recipes_output)
    # 8.) String formatieren und dem Label zuweisen
    recipes_string = "\n".join(recipes_output)
    label_recipes["text"] = recipes_string

# Buttons:
button_erase = Button(cook_frame,bg="red",fg="black", text="Felder leeren", command=eraseFields)
button_confirm = Button(cook_frame,bg="lime", fg="black", text="    Suche Rezepte    ", command=showRecipes)
button_recipe_info = Button(cook_frame, bg="orange", fg="black", text="Rezept-Info", command=recipeInfo)
checkbutton_vegetarian = Checkbutton(cook_frame, bg="lime", fg = "black", text="vegetarisch", variable=veggie)
checkbutton_vegan = Checkbutton(cook_frame, bg="lime", fg = "black", text="vegan", variable=vegan)

# Baue Umgebung:
cook_frame.pack(padx=20, pady=20)
label_title.grid(column=0,row=0, columnspan=4)
label_ingredient_1.grid(column=0, row=2)
text_ingredient_1.grid(column=1, row=2)
label_ingredient_2.grid(column=0, row=3)
text_ingredient_2.grid(column=1, row=3)
label_ingredient_3.grid(column=0, row=4)
text_ingredient_3.grid(column=1, row=4)
label_cooktime.grid(column=0, row=5)
text_cooktime.grid(column=1, row=5)
label_cooktime_minuten.grid(column=2, row=5)
checkbutton_vegetarian.grid(column=0, row=6, columnspan=2, pady=10)
checkbutton_vegan.grid(column=2, row=6, columnspan=2, pady=10)
button_confirm.grid(column=0, row=7, pady=10, padx=20, columnspan=4)
label_recipe_info.grid(column=0, row=8)
text_recipe_info.grid(column=1, row=8)
button_recipe_info.grid(column=2, row=8, columnspan=2, padx=20)
button_erase.grid(column=0, row=9, columnspan=2)

label_seperator.grid(column=0,row=10,columnspan=4)
label_recipe_title.grid(column=0, row=11, padx=20)
label_recipes.grid(column=0,row=12)
label_recipe_details_title.grid(column=1, row=11, columnspan=2)
label_recipe_details.grid(column=1, row=12, columnspan=2)

# Starte GUI:
what_2_cook.mainloop()
