#!/usr/bin/env python
# coding: utf-8

# In[6]:


import sys
import pandas as pd


# In[7]:


print(sys.version)


# In[2]:


pip install httpx


# In[2]:


import requests 
import random 
import pprint
import re
import time
from collections import defaultdict
from bs4 import BeautifulSoup
import numpy as np
import tqdm

import httpx
from selectolax.parser import HTMLParser


# In[3]:


url_du_site = "https://music.feedspot.com/jazz_blogs/"


# In[4]:


def fetch_and_parse(url, selector, attribute=None):
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()  # Raises exception for 4xx/5xx responses
            html = HTMLParser(response.text)
            if attribute:
                return [node.attributes[attribute] for node in html.css(selector)]
            else:
                return [node.text() for node in html.css(selector)]
    except httpx.HTTPStatusError as e:
        " "
    except Exception as e:
        " "
    return []


# In[5]:


titre = fetch_and_parse(url_du_site, "h1")[0]  # Extrait le premier titre h1
noms = fetch_and_parse(url_du_site, "h3")  # Extrait tous les textes h3
localisations = fetch_and_parse(url_du_site, '.location_new')  # Extrait les localisations
web = fetch_and_parse(url_du_site, '.ext', 'href')  # Extrait les URLs des liens externes
fbsub = fetch_and_parse(url_du_site, '.fs-facebook')
twitsub = fetch_and_parse(url_du_site, '.fs-twitter')
instasub = fetch_and_parse(url_du_site, '.fs-instagram')
print(titre)
print(noms)
print(localisations)
print(web)
print(fbsub)
print(twitsub)
print(instasub)


# In[6]:


def convertir_en_nombre(abonnes_str):
    # Supprime 'K', multiplie par 1000 si 'K' était présent
    if 'K' in abonnes_str:
        return int(float(abonnes_str.replace('K', '')) * 1000)
    return int(abonnes_str.replace('.', '').replace(',', ''))

# Application de la fonction optimisée sans besoin de prétraitement spécifique pour 'K'
fbsub_numerique = [convertir_en_nombre(abonne) for abonne in fbsub if 'K' in abonne]
twitsub_numerique = [convertir_en_nombre(abonne) for abonne in twitsub if 'K' in abonne]
instasub_numerique = [convertir_en_nombre(abonne) for abonne in instasub if 'K' in abonne]

print(fbsub_numerique)
print(twitsub_numerique)
print(instasub_numerique)


# In[7]:


print(type(titre),titre)

print(type(noms),noms)

print(type(localisations), localisations)

print(type(web), web)

print(type(fbsub_numerique), fbsub_numerique)

print(type(twitsub_numerique), twitsub_numerique)

print(type(instasub_numerique), instasub_numerique)


# In[47]:


type(titre)


# In[8]:


chemin = r"C:\Users\valen\Desktop\Python txt\mon_fichier.txt"  # Assurez-vous que le chemin mène à un fichier, pas un dossier

with open(chemin, "a") as f:  # "a" pour le mode append, ajoute au fichier s'il existe ou crée un nouveau fichier s'il n'existe pas
    f.write(f"{noms}\n")  # \n permet de sauter une ligne, un deuxième \n permet de laisser un espace
    f.write(f"{localisations}\n")
    f.write(f"{web}\n")
    f.write(f"{fbsub}\n")
    f.write(f"{twitsub}\n")
    f.write(f"{instasub}\n")


# In[10]:


import os

chemin = r"C:\Users\valen\Desktop\Python txt\mon_fichier2.txt"
with open(chemin, "a", encoding='utf-8') as fichier:
    fichier.write(f"{noms}\n")
    fichier.write(f"{localisations}\n")
    fichier.write(f"{web}\n")
    fichier.write(f"{fbsub_numerique}\n")
    fichier.write(f"{twitsub_numerique}\n")
    fichier.write(f"{instasub_numerique}\n")


# In[9]:


chemin = r"C:\Users\valen\Desktop\Python txt\mon_fichier2.txt"

# S'assurer que toutes les listes ont la même longueur
min_length = min(len(noms_propres), len(localisations), len(web), len(fbsub_numerique), len(twitsub_numerique), len(instasub_numerique))

with open(chemin, "a", encoding='utf-8') as fichier:
    for i in range(min_length):
        fichier.write(f"Nom: {noms_propres[i]}\n")
        fichier.write(f"Localisation: {localisations[i]}\n")
        fichier.write(f"Web: {web[i]}\n")
        fichier.write(f"Facebook: {fbsub_numerique[i] if i < len(fbsub_numerique) else 'N/A'}\n")
        fichier.write(f"Twitter: {twitsub_numerique[i] if i < len(twitsub_numerique) else 'N/A'}\n")
        fichier.write(f"Instagram: {instasub_numerique[i] if i < len(instasub_numerique) else 'N/A'}\n")
        fichier.write("\n")  # Ajoute un saut de ligne pour séparer les paragraphes

