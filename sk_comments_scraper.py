from bs4 import BeautifulSoup
import urllib.request
import re
import numpy as np

#smitten kitchen recipe index
sk_recipes_url = 'https://smittenkitchen.com/recipes/'

sk_index_html = urllib.request.urlopen(sk_recipes_url)
soup = BeautifulSoup(sk_index_html, 'html.parser')

#pull category html from index page
categories = soup.find_all("a", attrs={'href': re.compile("^https://smittenkitchen.com/recipes")})

num_categories = len(categories)
category_urls = []
temp_cat = 0

recipe_urls = []

for i in range(0, num_categories):
    # build list of all category url's
    temp_cat = categories[i]
    temp_cat_url = temp_cat.get('href')
    category_urls += [temp_cat_url]

    category_html = urllib.request.urlopen(temp_cat_url)
    soup_category = BeautifulSoup(category_html, 'html.parser')

    # build list of all the recipe urls per category
    recipes = soup_category.find_all("a", attrs={'rel': re.compile("^bookmark")})

    for j in range(0, len(recipes) - 1):

        recipe_url = recipes[j].get('href')

        if recipe_url not in recipe_urls:
            recipe_urls += [recipe_url]


# create list of all comments with indexing mapped to recipe url's
import pandas as pd

recipe_comment = ""
all_comments = [""] * len_recipe_urls
len_recipe_urls = len(recipe_urls)

for i in range(0, len_recipe_urls - 1):
    sk_recipe_html = urllib.request.urlopen(recipe_urls[i])
    soup_recipe = BeautifulSoup(sk_recipe_html, 'html.parser')

    # create a list of all comments with the recipe index i
    comments = soup_recipe.find_all(class_=re.compile("comment-content"))
    all_recipe_comments = ""

    for j in range(0, len(comments) - 1):
        recipe_comment = comments[j].get_text()
        all_recipe_comments += recipe_comment

    all_comments[i] = all_recipe_comments


np.savetxt("sk_comments.csv", all_comments, delimiter=",", fmt="%s")
