#!/usr/bin/env python
# coding: utf-8

# In[5]:


#importer les packages
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


url = "https://music.feedspot.com/jazz_blogs/"


# In[11]:


#importer les fonctions du script SCRAPb
get_ipython().run_line_magic('run', 'SCRAPb.ipynb')



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
    ville_reg_pays = get_ville_region_pays()  # ville, region et pays de chaque blogueur

    return [nom_blog, localisation, site_web, fbsub_num, twitsub_num, instasub_num, adresses_email, ville_reg_pays]

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
TableBlog = add_row_to_table(TableBlog, new_rowG)

print(TableBlog)


# In[69]:





# # PARTIE 2. Scrapper le site des festivals

# In[13]:


#importer les fonctions du script des festivals
get_ipython().run_line_magic('run', 'SCRAPf.ipynb')


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


get_ipython().run_line_magic('run', 'mailauto.ipynb')


# # PARTIE 4: appeller les 3 parties pour tout afficher

# In[18]:


def get_everything():
    get_bloggers(url)
    create_datablog()
    get_festivals
    get_ipython().run_line_magic('run', 'mailauto.ipynb')

get_everything()    


# In[ ]:




