#!/usr/bin/env python
# coding: utf-8

# In[5]:

#importation des packages
import sys
import requests 
import random 
import pprint
import re
import time
from collections import defaultdict
from bs4 import BeautifulSoup
import numpy as np
import tqdm
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# # PARTIE 1. Scrapper le site des bloguers

# In[10]:

# Correct import statements
from SCRAPb import get_url, get_names, get_locals, get_webs, get_followers, create_email

# Now, use these functions with the appropriate arguments
url = "https://music.feedspot.com/jazz_blogs/"

# Example function call
blog_urls = get_url(url)  # Assuming get_url function returns something you can use

# Call other functions similarly
names = get_names(url)
locals = get_locals(url)
webs = get_webs(url)

# For functions that require more than one argument
twitter_followers = get_followers(url, "fs-twitter")
facebook_followers = get_followers(url, "fs-facebook")
instagram_followers = get_followers(url, "fs-instagram")

# For functions that do not require arguments (assuming create_email doesn't need arguments)
emails = create_email()


# In[8]:


def get_bloggers(url):  # creer une fonction qui appelle des fonctions du script des blogueurs pour extraire les données

    get_url(url)
    nom_blog = get_names(url) #nom des blogs
    localisation = get_locals(url) #localisation des blogeurs
    site_web = get_webs(url) #sites web des blogeurs

    # abonnés sur Twitter, Facebook et Instagram
    twitsub = get_followers(url, "fs-twitter")
    fbsub = get_followers(url, "fs-facebook")
    instasub = get_followers(url, "fs-instagram")

    # abonnés convertis en nombre
    fbsub_num = [convertir_en_nombre(abonne) for abonne in fbsub]
    twitsub_num = [convertir_en_nombre(abonne) for abonne in twitsub]
    instasub_num = [convertir_en_nombre(abonne) for abonne in instasub]

    adresses_email = create_email()  # création des adresses mail pour chaque blogueur
    return [nom_blog, localisation, site_web, fbsub_num, twitsub_num, instasub_num, adresses_email]

# Appel de la fonction pour extraire les données
url = "https://music.feedspot.com/jazz_blogs/"
get_bloggers(url)


# In[12]:


def add_row_to_table(table, new_row):
    # Créer un DataFrame à partir de la nouvelle ligne
    new_df = pd.DataFrame([new_row])
    
    # Concaténer le DataFrame existant avec le nouveau DataFrame
    table = pd.concat([table, new_df], ignore_index=True)
    
    return table

def create_datablog():
    DataBlog = {"Nom Blog": nom_blog,
                "Pays": Pays,
                "Région": Region,
                "Ville": Ville,
                "Adresse Email": create_email(),
                "Site web": site_web,
                "Abonnées Facebook": fbsub_num,
                "Abonnées Twitter": twitsub_num,
                "Abonnées Instagram": instasub_num
                }

    TableBlog = pd.DataFrame(DataBlog)
    TableBlog["Pays"] = TableBlog["Pays"].replace({"US": "USA"})
    
    return TableBlog

# Créer le DataFrame initial
TableBlog = create_datablog()

# Ajouter la nouvelle ligne
new_rowG = {'Nom Blog': "Georgiana", 'Pays': "Romania" ,'Région': "none", 'Ville': "none", 'Adresse Email': "iogecor02@gmail.com", 
            'Site web': "none" ,'Abonnées Facebook': 0, 'Abonnées Twitter': 0, 'Abonnées Instagram': 0}
new_rowV = {'Nom Blog': "Valentin", 'Pays': "France" ,'Région': "none", 'Ville': "none", 'Adresse Email': "valentin.barthel@etu.unistra.fr", 
            'Site web': "none" ,'Abonnées Facebook': 0, 'Abonnées Twitter': 0, 'Abonnées Instagram': 0}
#new_rowP = {'Nom Blog': "Pierre Pelletier", 'Pays': "France" ,'Région': "none", 'Ville': "none", 'Adresse Email': "p.pelletier@unistra.fr", 
#           'Site web': "none" ,'Abonnées Facebook': 0, 'Abonnées Twitter': 0, 'Abonnées Instagram': 0}
TableBlog = add_row_to_table(TableBlog, new_rowG)
TableBlog = add_row_to_table(TableBlog, new_rowV)
#TableBlog = add_row_to_table(TableBlog, new_rowP)

print(TableBlog)


# In[69]:





# # PARTIE 2. Scrapper le site des festivals

# In[13]:
from SCRAPfest import get_all_pages, get_event_names, scrape_all_events


# In[16]:


#creer une fonction qui appelle les fonctions du script des festivals pour recuperer les donnees:
def get_festivals():
    get_all_pages()
    get_event_names(url)
    TableEvent = scrape_all_events()
    TableEvent["Pays_Event"] = TableEvent["Pays_Event"].replace({"United States": "USA"})
    print(TableEvent)
get_festivals()    


# # PARTIE 3: mail automatique

# In[17]:

from mailauto import format_blogger_email, format_event_list, send_jazz_event_invitations


# # PARTIE 4: appeller les 3 parties pour tout afficher

# In[18]:


def get_everything():
    get_bloggers(url)
    create_datablog()
    get_festivals()
    format_blogger_email(blog['Nom Blog'], followers, country)
    format_event_list(country_events)
    send_jazz_event_invitations("smtp.gmail.com", 465, "jazzyworld67@gmail.com", "ogunqrpjhigzwpfc", TableBlog, TableEvent)
    
get_everything()    





