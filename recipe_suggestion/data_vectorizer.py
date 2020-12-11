import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer


def create_ingredients_dict():
    cuisines_dict = {}
    cuisines = []
    ingredients = []
    with open('dataset/yummly.json') as in_file:
        data = json.load(in_file)
    
    for i in range(len(data)):
        curr_cuisine = data[i]['cuisine']
        ingredients_list = data[i]['ingredients']

        if curr_cuisine not in cuisines_dict.keys():
            cuisines.append(curr_cuisine)
            cuisines_dict[curr_cuisine] = ingredients_list
        else:
            curr_ingredients = cuisines_dict[curr_cuisine]
            curr_ingredients.extend(ingredients_list)
            cuisines_dict[curr_cuisine] = curr_ingredients
        ingredients.extend(curr_ingredients)
    
    unique_ingredients = list(set(ingredients))
    num_unique_ingredients = len(unique_ingredients)
    num_cuisines = len(cuisines)

    return cuisines_dict, cuisines, num_cuisines, unique_ingredients, num_unique_ingredients

def create_count_vectors(num_cuisines, num_unique_ingredients, cuisine, cuisines_dict, ingredients):
    counts = np.zeros(num_cuisines, num_unique_ingredients)
    row = 0
    for c in cuisine:
        curr_ingredients = cuisines_dict[c]

        for ingredient in curr_ingredients:
            col = ingredients.index(ingredient)
            counts[row,col] += 1
        row += 1
    return counts