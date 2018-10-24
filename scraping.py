# --- Import packages --- #

import re # To clean strings
import pandas as pd # To manipulate df
import requests # To get page content
from lxml import html # To access html tree

# --- Get all index pages --- #

# Get page content
page = requests.get ('xxx')
htmltree = html.fromstring(page.content)

# Get main elements
link = htmltree.xpath('//div[@class="xxx"]/a/@href')
size = htmltree.xpath('//div[@class="xxx"]/text()')

# Get values from strings
size_num = [int(re.sub(' drinks', '', s)) for s in size] # get the total number of drinks on each category

# Create the new list
v_link= []

# Get all links, and then all possible pages to create all full links
for i,l in enumerate(link):
    for value in range(int(((size_num[i]/10) // 1 + 1))): # 10 drinks per page
        new_link = l + "?page=" + str(value+1) # Enumerate begin at 0 and pages list at 1
        v_link.append(new_link)
        
        
        
# --- Scrap a page --- #

def getDfRecipe(pagelink):
    '''
    Goal: Get main informations (Drinks Names, Ingredient & Quantity, Recipe) from a recipe web page.
    Input: url link
    Output: Dataframe - Cocktail recipe (1 row by ingredient)
    To do: Raise an error if link not in link with the website
    '''
    
    # Get page content
    page = requests.get(pagelink)
    htmltree = html.fromstring(page.content)
    
    # Get main elements
    name = htmltree.xpath('//div[@class="xxx"]/text()')
    qte = htmltree.xpath('//div[@class="xxx"]/text()')
    ingred = htmltree.xpath('//div[@class="xxx"]/text()')
    recipe = htmltree.xpath('//div[@class="xxx"]/text()')
    
    try:
        
        # Pre-formating information
        v_name = name * len(ingred)
        merged_recipe = re.sub('\t|\r|\n', '', ' '.join(recipe))
        v_recipe = [merged_recipe] * len(ingred)
        
        # Deal with no quantity
        error = ['No']* len(ingred)
        if len(qte)<len(ingred):
            [qte.append('') for x in range(len(ingred)-len(qte))]
            error = ['Yes']* len(ingred)
    
        # Create sub-df
        new_df = pd.DataFrame({'Cocktail': v_name, 'Quantity': qte, 'Ingredient': ingred, 'Recipe': v_recipe, 'Issue': error})
        return new_df
    
    except ValueError:
        print("ValueError here")
