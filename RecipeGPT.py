from Recipes import AllRecipes
import requests
import json

#Ingredients list for which to request prompt. Index start = 0
RecipeNo = 0

#Setting up chatGPT API
api_endpoint = "https://api.openai.com/v1/completions"
f = open("APIkey.json")
headers = json.load(f)

DishesDict = AllRecipes[RecipeNo].dishes
for Dish in DishesDict:
    Dish = Dish
    Ingredients = DishesDict[Dish]
    IngredientsStr = ""
    for ingredient in Ingredients:
        IngredientsStr += f" {ingredient},"
    IngredientsStr = IngredientsStr[0:-1]
    print(IngredientsStr)
    ChatGPTPrompt = f"Kun je een recept maken voor {Dish} 4 personen met de volgende ingredienten: {IngredientsStr}. Maak daarna een woordgrap over een van de ingredienten. Temperatuur in graden celcius. Geef in het begin aan dat het recept voor 4 personen is en verzin er een naam bij met een woordspeling met een van de ingredienten."

    request_data = {
        "model": "text-davinci-003",
        "prompt": f"{ChatGPTPrompt}",
        "max_tokens": 500
    }

    response = requests.post(api_endpoint, headers=headers, json=request_data)
    if response.status_code == 200: 
        print(response.json()["choices"][0]["text"])
        print(response.json())
    else:
        print(response)

f.close()