# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:01:57 2023

@author: gidos
"""

import yaml

class Recipe:
    def __init__(self, name):
        self.name = name

    def week(self, week):
        self.week = week

    def dishes(self, dishes):
        self.dishes = dishes

    def rating(self, rating):
        self.rating = rating
        self.avgRating = sum(rating.values())/len(rating)

    def photo(self, photo):
        self.photo = photo

    def recipes(self, recipes):
        self.recipes = recipes
    
recipes = yaml.load(open(r"Recipes.yaml"), Loader=yaml.FullLoader)

AllRecipes = []
for ii in range(len(recipes)):
    RecipeObj  = Recipe(recipes[ii]['name'])
    RecipeObj.week(recipes[ii]['week'])
    RecipeObj.rating(recipes[ii]['rating'])
    RecipeObj.photo(recipes[ii]['photo'])
    RecipeObj.dishes(recipes[ii]['dishes'])
    RecipeObj.recipes(recipes[ii]['recipes'])
    AllRecipes.append(RecipeObj)

